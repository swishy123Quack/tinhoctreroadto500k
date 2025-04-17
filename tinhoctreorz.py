import subprocess
import threading

NO_PROCESS = 2 
def run_script(name):
    subprocess.run(["python", name])

threads = []
for script in range(NO_PROCESS):
    t = threading.Thread(target=run_script, args=('run.py',))
    t.start()
    threads.append(t)

for t in threads:
    t.join()