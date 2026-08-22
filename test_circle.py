import math
def sub(a,b): return [a[0]-b[0],a[1]-b[1],a[2]-b[2]]
def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def length(a): return math.sqrt(dot(a,a))
def norm(a):
    l=length(a) or 1; return [a[0]/l,a[1]/l,a[2]/l]

def fitCircle(A,B,C):
    ab=sub(B,A); ac=sub(C,A); abXac=cross(ab,ac)
    denom=2*dot(abXac,abXac)
    if denom<1e-9: return None
    t=[(cross(abXac,ab)[i]*dot(ac,ac)+cross(ac,abXac)[i]*dot(ab,ab))/denom for i in range(3)]
    center=[A[i]+t[i] for i in range(3)]
    return center, length(t), norm(abXac)

# Known circle: center C0, radius R, tilted plane spanned by u,v (orthonormal)
C0=[3.0,4.0,5.0]; R=15.0
u=norm([1.0,1.0,0.0]); 
n=norm([1.0,-1.0,2.0])
v=norm(cross(n,u))   # v perpendicular to u, in plane perpendicular to n
# ensure u perp v perp: recompute u as cross(v,n)
u=norm(cross(v,n))
def pt(theta):
    return [C0[i]+R*(math.cos(theta)*u[i]+math.sin(theta)*v[i]) for i in range(3)]

for angles in [(0.3,2.0,4.5),(0.0,2.094,4.188)]:
    A,B,Cc=pt(angles[0]),pt(angles[1]),pt(angles[2])
    center,rad,normal=fitCircle(A,B,Cc)
    print(f"angles={angles}  center=({center[0]:.4f},{center[1]:.4f},{center[2]:.4f})  radius={rad:.4f}")

# collinear guard test
print("collinear ->", fitCircle([0,0,0],[1,1,1],[2,2,2]))
