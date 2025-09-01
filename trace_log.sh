#!/bin/bash
sudo cat /sys/kernel/debug/tracing/trace_pipe | sudo tee -a trace.log
