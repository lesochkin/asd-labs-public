import time,sys,json,subprocess
from main_overlap_time import mainFun 
from pathlib import Path

def run_argv(argv, **kw):
    kw.setdefault("encoding", "utf-8")
    kw.setdefault("errors", "replace")
    return subprocess.run(argv, **kw)

path=Path(r".\r1-session-log\test_info.json")
gen_info=json.loads(path.read_text(encoding="utf-8"))

def gener(c):
    Nomer=c if c>1 else "10000"
    r = run_argv([sys.executable, str(Path(gen_info["gen"])),str(Nomer)]+gen_info["stamps"],
                capture_output=True, text=True)

    with open(gen_info["in_path"], "w", encoding="utf-8",errors='replace') as filik:
        filik.write(r.stdout)

if __name__=='__main__':
    gener(10000)
    for _ in range(3):
        mainFun(gen_info["in_path"],gen_info["out_path"]) 

    c=10000
    for _ in range(6):
        gener(c)
        arr=[]
        for x in range(11):
            start=time.perf_counter()
            mainFun(gen_info["in_path"],gen_info["out_path"]) 
            end=time.perf_counter()
            arr.append((end-start)*1000)
        arr.sort()
        print(c,f'\tavg={arr[5]:.3f}\tznach=',*[f'{c:.3f}'for c in arr], f'f={arr[5]/c/2}')
        c*=2

    # .write_text(r.stdout, encoding="utf-8")
    # print(r["gen"])