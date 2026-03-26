class SubarrayMeanCalculator:

    def read_integer_list(self):
        return list(map(int, input().split()))

    def read_numbers(self):
        return list(map(int, input().split()))

    def create_prefix_sums(self, numbers):
        prefix_sums = [0] * (len(numbers) + 1)
        for position in range(1, len(numbers) + 1):
            prefix_sums[position] = prefix_sums[position - 1] + numbers[position - 1]
        return prefix_sums

    def compute_floor_mean(self, prefix_sums, left, right):
        subarray_sum = prefix_sums[right] - prefix_sums[left - 1]
        subarray_length = right - left + 1
        return subarray_sum // subarray_length

    def answer_queries(self, prefix_sums, total_queries):
        for _ in range(total_queries):
            left, right = self.read_integer_list()
            print(self.compute_floor_mean(prefix_sums, left, right))

    def execute(self):
        element_count, query_count = self.read_integer_list()
        numbers = self.read_numbers()
        prefix_sums = self.create_prefix_sums(numbers)
        self.answer_queries(prefix_sums, query_count)

if __name__ == "__main__":
    SubarrayMeanCalculator().execute()
