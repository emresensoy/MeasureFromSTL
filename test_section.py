import math
R,L,seg=10.0,50.0,160
z0,z1=5.0,55.0
def ring(z): return [(R*math.cos(2*math.pi*i/seg),R*math.sin(2*math.pi*i/seg),z) for i in range(seg)]
bot,top=ring(z0),ring(z1); cb,ct=(0,0,z0),(0,0,z1)
tris=[]
for i in range(seg):
    j=(i+1)%seg
    tris.append((bot[i],bot[j],top[j])); tris.append((bot[i],top[j],top[i]))
    tris.append((cb,bot[j],bot[i])); tris.append((ct,top[i],top[j]))

def section(n,c):
    E=[(0,1),(1,2),(2,0)]; segs=[]
    for P in tris:
        d=[P[0][n]-c,P[1][n]-c,P[2][n]-c]
        hits=[]
        for i,j in E:
            di,dj=d[i],d[j]
            if (di<0 and dj>=0) or (di>=0 and dj<0):
                tt=di/(di-dj)
                hits.append(tuple(P[i][k]+(P[j][k]-P[i][k])*tt for k in range(3)))
        if len(hits)==2: segs.append(hits)
    return segs

def bbox(segs,u,v):
    us=[p[u] for s in segs for p in s]; vs=[p[v] for s in segs for p in s]
    return max(us)-min(us), max(vs)-min(vs), len(segs)

# normal Z (=2) at center z=30 -> plane XY, u=0(X),v=1(Y)
s=section(2,30.0); w,h,n=bbox(s,0,1)
print(f"Z-normal @30 -> width(X)={w:.3f} height(Y)={h:.3f} segs={n}  (expect ~20 x ~20)")
# normal X (=0) at x=0 -> u=1(Y),v=2(Z)
s=section(0,0.0); w,h,n=bbox(s,1,2)
print(f"X-normal @0  -> width(Y)={w:.3f} height(Z)={h:.3f} segs={n}  (expect ~20 x 50)")
# normal Z outside the part -> empty
s=section(2,100.0); print(f"Z-normal @100 -> segs={len(s)} (expect 0)")
