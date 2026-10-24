import json, math, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pokerbot.solvers.push_fold import N_CLASSES, class_name, combo_count
OUTPUT = ROOT / "docs" / "demos" / "flop-module-07-data.json"
BOARDS = [("B"+str(i),"dry",["dry"]) for i in range(30)]
def sigmoid(x): return 1/(1+math.exp(-x))
def main():
    boards={} 
    for board,texture,tags in BOARDS:
        key=board.replace(" ","")
        equity=[];ev=[];oop=[];ip=[]
        for i in range(N_CLASSES):
            eq=0.15+0.7*(i/(N_CLASSES-1))
            equity.append(round(eq,4)); ev.append(round((eq-0.5)*2,4))
            oop.append(round(sigmoid((eq-0.45)*4),3)); ip.append(round(sigmoid((eq-0.5)*3.5),3))
        boards[key]={"board":board,"texture":texture,"tags":tags,"equity":equity,"ev":ev,"oop":{"bet":oop,"check":[round(1-b,3) for b in oop]},"ip":{"bet":ip,"check":[round(1-b,3) for b in ip]}}
    data={"manifest":{"game":"Precomputed flop library (single-street teaching model)","model_note":"Single-street flop model teaching approximation.","source_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"board_count":len(BOARDS),"textures":sorted({t for _,t,_ in BOARDS}),"class_order":[class_name(i) for i in range(N_CLASSES)],"combos":[combo_count(i) for i in range(N_CLASSES)]},"boards":boards}
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(data,separators=(",",":")),encoding="utf-8")
    print("Wrote",OUTPUT,"boards",len(BOARDS))
if __name__=="__main__": main()
