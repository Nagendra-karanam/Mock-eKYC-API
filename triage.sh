#!/bin/bash

NAMESPACE=$1
OUTPUT="triage-logs.txt"

if [ -z "$NAMESPACE" ]; then
  echo "Usage: ./triage.sh <namespace>"
  exit 1
fi

> $OUTPUT

for pod in $(kubectl get pods -n $NAMESPACE --no-headers | awk '/CrashLoopBackOff/ {print $1}')
do
  echo "===== Logs for $pod =====" >> $OUTPUT
  kubectl logs -n $NAMESPACE $pod --tail=50 >> $OUTPUT
  echo "" >> $OUTPUT
done

echo "Logs saved to $OUTPUT"
