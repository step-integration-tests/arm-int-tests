FROM --platform=linux/x86_64 amazonlinux:2

FROM amazonlinux:2023 as build_env

FROM python:3.12.2-slim

FROM gcr.io/google.com/cloudsdktool/cloud-sdk:456.0.0

FROM ghcr.io/aquasecurity/trivy:0.48.0

FROM mcr.microsoft.com/dotnet/runtime:8.0.3 AS dotnet_runtime

# ------------------------------------------------

FROM amazonlinux:2023

RUN yum install -y python3

FROM alpine:3.18.6

RUN apk add --no-cache bash

FROM python:3.7.17

RUN pip install requests

RUN useradd --system --create-home --shell /bin/bash clamavuser

EXPOSE 8000
USER clamavuser
WORKDIR /home/clamavuser

ENV PATH="/home/clamavuser/.local/bin:${PATH}"
RUN \
    python -m pip install --user setuptools
RUN \
    python -m pip install --user cvdupdate==1.1.1 && \
    cvd update
