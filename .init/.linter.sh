#!/bin/bash
cd /home/kavia/workspace/code-generation/event-planner-and-reminder-app-169652-171295/event_manager_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

