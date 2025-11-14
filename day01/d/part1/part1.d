#!/usr/bin/env rdmd

import std.algorithm;
import std.array;
import std.conv;
import std.file;
import std.stdio;
import std.string;

int get_sum(const string group)
{
    return group.splitLines.map!(to!int).sum;
}

void main()
{
    // const fname = "example.txt";
    const fname = "input.txt";

    const groups = readText(fname).split("\n\n");
    const values = groups.map!(gr => get_sum(gr)).array;

    writeln(values.maxElement);
}
