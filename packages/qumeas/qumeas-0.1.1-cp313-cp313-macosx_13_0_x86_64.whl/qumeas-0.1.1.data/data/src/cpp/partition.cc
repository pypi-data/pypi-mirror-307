#include "qumeas/partition.h"
#include <iostream>
#include <vector>
#include <queue>
#include <thread>
#include <future>
#include <mutex>
#include <condition_variable>
#include <algorithm>

// TaskQueue methods
void TaskQueue::push(const Task& task) {
    {
        std::lock_guard<std::mutex> lock(mutex_);
        tasks_.push(task);
    }
    cond_var_.notify_one();
}

bool TaskQueue::pop(Task& task) {
    std::unique_lock<std::mutex> lock(mutex_);
    while (tasks_.empty() && !done_) {
        cond_var_.wait(lock);
    }
    if (!tasks_.empty()) {
        task = tasks_.front();
        tasks_.pop();
        return true;
    }
    return false;
}

void TaskQueue::set_done() {
    {
        std::lock_guard<std::mutex> lock(mutex_);
        done_ = true;
    }
    cond_var_.notify_all();
}

// Generate non-crossing partitions in a multithreaded environment
void _make_non_crossing_partitions_mt(
    std::vector<int> elements,
    std::vector<std::vector<int>>& active_partitions,
    std::vector<std::vector<int>>& inactive_partitions,
    int max_size,
    std::vector<std::vector<std::vector<int>>>& all_partitions,
    std::mutex& result_mutex
) {
    if (elements.empty()) {
        std::vector<std::vector<int>> full_partition = active_partitions;
        full_partition.insert(full_partition.end(), inactive_partitions.begin(), inactive_partitions.end());
        std::lock_guard<std::mutex> lock(result_mutex);
        all_partitions.push_back(full_partition);
        return;
    }

    int elem = elements.back();
    elements.pop_back();

    // Option 1: Create a new partition with the current element
    if (1 <= max_size) {
        active_partitions.push_back({elem});
        _make_non_crossing_partitions_mt(elements, active_partitions, inactive_partitions, max_size, all_partitions, result_mutex);
        active_partitions.pop_back();
    }

    // Option 2: Add element to existing partitions within max_size constraint
    size_t original_size = active_partitions.size();
    for (size_t i = original_size; i-- > 0;) {
        if (active_partitions[i].size() < max_size) {
            active_partitions[i].push_back(elem);
            _make_non_crossing_partitions_mt(elements, active_partitions, inactive_partitions, max_size, all_partitions, result_mutex);
            active_partitions[i].pop_back();
        }
        
        // Move partition to inactive to avoid crossings in subsequent partitions
        inactive_partitions.push_back(std::move(active_partitions.back()));
        active_partitions.pop_back();
    }

    // Restore active partitions from inactive
    for (size_t i = 0; i < original_size; ++i) {
        active_partitions.push_back(std::move(inactive_partitions.back()));
        inactive_partitions.pop_back();
    }
    
    // Restore elements for backtracking
    elements.push_back(elem); 
}

// Worker function for each thread in the thread pool
void worker_function(
    TaskQueue& task_queue,
    std::vector<std::vector<std::vector<std::vector<int>>>>& all_partitions,
    std::mutex& result_mutex,
    int max_size
) {
    Task task;
    while (task_queue.pop(task)) {
        // Local container to collect partitions 
        std::vector<std::vector<std::vector<int>>> partitions;

        // Generate all non-crossing partitions 
        std::vector<std::vector<int>> active_partitions;
        std::vector<std::vector<int>> inactive_partitions;
        _make_non_crossing_partitions_mt(task.elements, active_partitions, inactive_partitions, max_size, partitions, result_mutex);

        // Add the result to the shared vector at the correct index
        {
            std::lock_guard<std::mutex> lock(result_mutex);
            all_partitions[task.index] = std::move(partitions);
        }
    }
}

// Main function 
void generate_partition_non_crossing(
    const std::vector<std::vector<int>>& list_of_lists,
    int max_size,
    int num_threads,
    std::vector<std::vector<std::vector<std::vector<int>>>>& all_partitions
) {
    TaskQueue task_queue;
    std::mutex result_mutex;
    std::vector<std::thread> threads;

    // Resize all_partitions 
    all_partitions.resize(list_of_lists.size());

    // Start worker threads
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(worker_function,
                             std::ref(task_queue),
                             std::ref(all_partitions),
                             std::ref(result_mutex),
                             max_size);
    }

    // Queue tasks 
    for (size_t i = 0; i < list_of_lists.size(); ++i) {
        Task task;
        task.index = i;
        task.elements = list_of_lists[i];
        task_queue.push(task);
    }

    // Signal queued
    task_queue.set_done();

    // Wait to finish
    for (auto& t : threads) {
        t.join();
    }
}
