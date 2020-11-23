#!/bin/bash

celery -A background worker -B --loglevel=INFO