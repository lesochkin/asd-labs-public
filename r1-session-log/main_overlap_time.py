import sys,os,string
def mainFun(InPath,OutPath):
    vrem=[]
    ABC={}
    flag=0
    sessions=1
    sum_time=0
    enters=0
    peak=[0,0]
    with open(InPath, "r", encoding="utf-8",errors='replace') as file:
        with open(OutPath, "w+", encoding="utf-8") as myfile:
            content = file.read().split('\n')
            for x in range(len(content)):
                if content[x]=='':
                    continue
                content[x]=content[x].split()
                if len(content[x])<=2 or len(content[x])>3 or not content[x][2].isdigit():
                    myfile.write(f"ERROR {x+1} bad_event\n")
                    continue
                if (content[x][1] not in ABC) and (content[x][0]=="LOGIN" or content[x][0]=="LOGOUT"):
                    vrem.append([content[x][1],'0','0','0', 0])
                    ABC[content[x][1]]=len(ABC)
                elif content[x][1] not in ABC:
                    myfile.write(f"ERROR {x+1} bad_event\n")
                    continue
                temp=ABC[content[x][1]]

                if content[x][0]=="LOGIN":
                    if int(vrem[temp][1])-int(vrem[temp][2])==0:
                        vrem[temp][1]=str(int(vrem[temp][1])+1)
                        vrem[temp][3]=str(x+1)
                        enters+=1
                        if peak[1]<enters:
                            peak[1]=enters
                            peak[0]=x+1
                        vrem[temp][4]=int(content[x][2])
                    elif int(vrem[temp][1])-int(vrem[temp][2])>0:
                        myfile.write(f'ERROR {x+1} invalid_login\n')
                elif content[x][0]=="LOGOUT":
                    if vrem[temp][1]==vrem[temp][2]:
                        myfile.write(f'ERROR {x+1} logout_without_login\n')
                    else:
                        vrem[temp][2]=str(int(vrem[temp][2])+1)
                        enters-=1
                        sessions+=1
                        sum_time+=int(content[x][2])-vrem[temp][4]

            for x in range(len(vrem)):
                if vrem[x][3]!='0' and vrem[x][1]>vrem[x][2]:
                    myfile.write(f'ERROR {vrem[x][3]} session_not_closed\n')
            myfile.write('SESSIONS '+str(sum([int(vrem[x][2])for x in range(len(vrem))])))
    if __name__=="__main__":
        print(f"# stats: peak_concurrent={peak[1]} at line={peak[0]}", file=sys.stderr)
        if sessions!=0:
            avg=sum_time/sessions
            print(f"# stats: avg_duration={avg:.3f}", file=sys.stderr)
        else: print(f"# stats: avg_duration=ERROR", file=sys.stderr)
if __name__=="__main__":
    mainFun(sys.argv[1],sys.argv[2])