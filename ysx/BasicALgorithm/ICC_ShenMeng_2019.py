"""
Paper Title: 《Webpage Fingerprinting Using Only Packet Length Information》 ICC ShenMeng

Description:
    This Python file contains an implementation of a feature extraction algorithm
    designed for analyzing network traffic. The algorithm processes packet lengths
    in a flow, computes cumulative lengths, and extracts feature sets based on
    interval hashing.

Author: [ysx]
Date: [2024.5.6]
Version: 1.0.0

Functions:
    hash_interval(start, end):
        Computes a hash value for a given interval defined by `start` and `end`.

    feature_extraction(flow, num_intervals=5):
        Extracts feature sets from a given flow based on cumulative packet lengths
        and interval hashing.

Example Usage:
    flow = [100, 200, 150, 250, 300]
    feature_set = feature_extraction(flow, num_intervals=3)
    print("Feature Set:", feature_set)

Notes:
    - Ensure that packet lengths provided in the `flow` list are positive integers.
    - Adjust `num_intervals` to control the granularity of interval hashing.

Todo:
    - Implement additional feature extraction techniques for enhanced traffic analysis.
    - Integrate this algorithm with a machine learning classifier for web traffic classification.

"""

import hashlib

def hash_interval(start, end):
    """
    Computes a hash value for a given interval defined by `start` and `end`.

    Parameters:
        start (int): The starting point of the interval.
        end (int): The ending point of the interval.

    Returns:
        str: A SHA-256 hash value representing the interval.
    """
    return hashlib.sha256(f"{start}-{end}".encode()).hexdigest()


def feature_extraction(flow, num_intervals=5):
    """
    Extracts feature sets from a given flow based on cumulative packet lengths
    and interval hashing.

    Parameters:
        flow (list): A list of packet lengths in the flow.
        num_intervals (int): The number of intervals to divide the cumulative lengths.

    Returns:
        tuple: The interval hash with the maximum count and its corresponding count.
    """
    cumulative_lengths = [sum(flow[:i + 1]) for i in range(len(flow))]

    min_length = min(cumulative_lengths)
    max_length = max(cumulative_lengths)
    interval_ranges = []

    interval_step = (max_length - min_length) // num_intervals
    for i in range(num_intervals):
        start = min_length + i * interval_step
        end = min_length + (i + 1) * interval_step
        interval_ranges.append((start, end))

    interval_ranges.append((interval_ranges[-1][1], max_length + 1))

    interval_map = {}
    for start, end in interval_ranges:
        interval_hash = hash_interval(start, end)
        interval_map[interval_hash] = (start, end)

    count_dict = {interval_hash: 0 for interval_hash in interval_map}

    for length in cumulative_lengths:
        for interval_hash, (start, end) in interval_map.items():
            if start <= length < end:
                count_dict[interval_hash] += 1
                break

    max_count = max(count_dict.values())
    max_hash = max(count_dict, key=count_dict.get)

    return (max_hash, max_count)


# Example usage
if __name__ == "__main__":
    flow = [100, 200, 150, 250, 300]
    feature_set = feature_extraction(flow, num_intervals=3)
    print("Feature Set:", feature_set)
