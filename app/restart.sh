until python3 launcher.py; do
    echo "launcher crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
