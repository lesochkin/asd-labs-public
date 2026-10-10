import sys,os,string

vrem=[]
ABC={}
flag=0
kol_vo=0
peak=[0,0]
with open(sys.argv[1], "r", encoding="utf-8") as file:
    with open((sys.argv[2]), "w+", encoding="utf-8") as myfile:
        content = file.read().split('\n')
        for x in range(len(content)):
            if content[x]=='':
                continue
            content[x]=content[x].split()
            if len(content[x])<=1:
                myfile.write(f"ERROR {x+1} bad_event\n")
                continue
            if (content[x][1] not in ABC) and (content[x][0]=="LOGIN" or content[x][0]=="LOGOUT"):
                vrem.append([content[x][1],'0','0','0'])
                ABC[content[x][1]]=len(ABC)
            elif content[x][1] not in ABC:
                myfile.write(f"ERROR {x+1} bad_event\n")
                continue
            temp=ABC[content[x][1]]

            if content[x][0]=="LOGIN":
                if int(vrem[temp][1])-int(vrem[temp][2])==0:
                    vrem[temp][1]=str(int(vrem[temp][1])+1)
                    vrem[temp][3]=str(x+1)
                    kol_vo+=1
                    if peak[1]<kol_vo:
                        peak[1]=kol_vo
                        peak[0]=x+1
                elif int(vrem[temp][1])-int(vrem[temp][2])>0:
                    myfile.write(f'ERROR {x+1} invalid_login\n')
            elif content[x][0]=="LOGOUT":
                if vrem[temp][1]==vrem[temp][2]:
                    myfile.write(f'ERROR {x+1} logout_without_login\n')
                else:
                    vrem[temp][2]=str(int(vrem[temp][2])+1)
                    kol_vo-=1

        for x in range(len(vrem)):
            if vrem[x][3]!='0' and vrem[x][1]>vrem[x][2]:
                myfile.write(f'ERROR {vrem[x][3]} session_not_closed\n')
        myfile.write('SESSIONS '+str(sum([int(vrem[x][2])for x in range(len(vrem))])))
print(f"stats: peak_concurrent={peak[1]} at line={peak[0]}", file=sys.stderr)