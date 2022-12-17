#!/usr/bin/env python3


def merge_intervals(intervals):
    # Sort the array on the basis of start values of intervals.
    intervals.sort()
    stack = []
    # insert first interval into stack
    stack.append(intervals[0])
    for curr in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if stack[-1][0] <= curr[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], curr[-1])
        else:
            stack.append(curr)

    return stack


def main():
    li = [[12, 12], [2, 14], [2, 2], [0, 2], [16, 20], [14, 18]]
    result = merge_intervals(li)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
