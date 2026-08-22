import math

# Build a cylinder mesh: radius R=10, length L=50, axis = Z, centered offset to test bbox center
R, L, seg = 10.0, 50.0, 120
z0, z1 = 5.0, 55.0  # length 50 along Z
tris = []  # each tri = (v0,v1,v2)

def ring(z):
    return [(R*math.cos(2*math.pi*i/seg), R*math.sin(2*math.pi*i/seg), z) for i in range(seg)]

bot, top = ring(z0), ring(z1)
cb, ct = (0,0,z0), (0,0,z1)
for i in range(seg):
    j=(i+1)%seg
    # side quad -> 2 tris
    tris.append((bot[i],bot[j],top[j]))
    tris.append((bot[i],top[j],top[i]))
    # caps
    tris.append((cb,bot[j],bot[i]))
    tris.append((ct,top[i],top[j]))

# ---- replicate computeStats ----
verts=[c for t in tris for v in t for c in v]  # flat
n=len(verts)//3
minv=[math.inf]*3; maxv=[-math.inf]*3
for i in range(n):
    for a in range(3):
        val=verts[i*3+a]
        minv[a]=min(minv[a],val); maxv[a]=max(maxv[a],val)
size=[maxv[a]-minv[a] for a in range(3)]
center=[(minv[a]+maxv[a])/2 for a in range(3)]
diag=math.hypot(*size)

# volume via signed tetrahedra
vol6=0.0
for t in tris:
    (ax,ay,az),(bx,by,bz),(cx,cy,cz)=t
    vol6 += ax*(by*cz-bz*cy) - ay*(bx*cz-bz*cx) + az*(bx*cy-by*cx)
volume=abs(vol6)/6

# ---- replicate diameterForAxis (axis=Z index 2) ----
def diameter(axis):
    a=(axis+1)%3; b=(axis+2)%3
    ca,cb=center[a],center[b]
    rs=[]
    for i in range(n):
        da=verts[i*3+a]-ca; db=verts[i*3+b]-cb
        rs.append(math.hypot(da,db))
    rs.sort()
    p99=rs[min(n-1,int(0.99*(n-1)))]
    return p99*2, max(rs)*2

len_axis=size.index(max(size))
dia_p99,dia_max=diameter(len_axis)

print(f"bbox size  X={size[0]:.3f} Y={size[1]:.3f} Z={size[2]:.3f}")
print(f"length axis index={len_axis} (0=X,1=Y,2=Z)  length={size[len_axis]:.3f}  (expect 50)")
print(f"diameter p99={dia_p99:.3f}  max={dia_max:.3f}  (expect ~20)")
print(f"volume={volume:.1f} mm3  (expect ~{math.pi*R*R*L:.1f})")
print(f"triangles={len(tris)}")
