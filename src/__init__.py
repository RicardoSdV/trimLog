"""
Example of what happens to compress lines:


    lines = ['X', 'Y', 'Z', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'B', 'C']


    compressed_lines = [X, Y, Z, [A], [[A], B], C]

    prettyfied_printed_lines =

    X
    Y
    Z
    2x
        A
    2x
        2x
            A
        B
    C

"""