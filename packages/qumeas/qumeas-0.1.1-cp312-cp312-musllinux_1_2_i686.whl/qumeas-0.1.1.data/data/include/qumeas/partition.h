#ifndef PARTITION_H
#define PARTITION_H

#include <vector>
#include <mutex>
#include <queue>
#include <condition_variable>

extern std::mutex mutex;

struct Task {
    size_t index;
    std::vector<int> elements;
};

class TaskQueue {
public:
    void push(const Task& task);
    bool pop(Task& task);
    void set_done();

private:
    std::queue<Task> tasks_;
    std::mutex mutex_;
    std::condition_variable cond_var_;
    bool done_ = false;
};

void _make_non_crossing_partitions_mt(
    const std::vector<int>& elements,
    std::vector<int> remaining_elements,
    std::vector<std::vector<int>> active_partitions,
    std::vector<std::vector<int>> inactive_partitions,
    int max_size,
    std::vector<std::vector<std::vector<int>>>& all_partitions,
    std::mutex& result_mutex
);

void worker_function(
    TaskQueue& task_queue,
    std::vector<std::vector<std::vector<std::vector<int>>>>& all_partitions,
    std::mutex& result_mutex,
    int max_size
);

void generate_partition_non_crossing(
    const std::vector<std::vector<int>>& list_of_lists,
    int max_size,
    int num_threads,
    std::vector<std::vector<std::vector<std::vector<int>>>>& all_partitions
);


#endif 

