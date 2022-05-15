from scene import Scene
import taichi as ti
from taichi.math import *
scene = Scene(voxel_edges=0.01, exposure=1)
scene.set_floor(-64, (1,1,1)) 
scene.set_background_color((135/255.,206/255.,235/255.)) # sky 
@ti.func
def rgb(r,g,b):
    return vec3(r/255.0, g/255.0, b/255.0)
@ti.func
def proj_plane(o, n, t, p): 
    y = dot(p-o,n);xz=p-(o+n*y);bt=cross(t,n);return vec3(dot(xz,t), y, dot(xz, bt))
@ti.func
def elli(rx,ry,rz,p1_unused,p2_unused,p3_unused,p):
    r = p/vec3(rx,ry,rz); return ti.sqrt(dot(r,r))<1
@ti.func
def cyli(r1,h,r2,round, cone, hole_unused, p):
    ms=min(r1,min(h,r2));rr=ms*round;rt=mix(cone*(max(ms-rr,0)),0,float(h-p.y)*0.5/h);r=vec2(p.x/r1,p.z/r2)
    d=vec2((r.norm()-1.0)*ms+rt,ti.abs(p.y)-h)+rr; return min(max(d.x,d.y),0.0)+max(d,0.0).norm()-rr<0
@ti.func
def box(x, y, z, round, cone, unused, p):
    ms=min(x,min(y,z));rr=ms*round;rt=mix(cone*(max(ms-rr,0)),0,float(y-p.y)*0.5/y);q=ti.abs(p)-vec3(x-rt,y,z-rt)+rr
    return ti.max(q, 0.0).norm() + ti.min(ti.max(q.x, ti.max(q.y, q.z)), 0.0) - rr< 0
@ti.func
def tri(r1, h, r2, round_unused, cone, vertex, p):
    r = vec3(p.x/r1, p.y, p.z/r2);rt=mix(1.0-cone,1.0,float(h-p.y)*0.5/h);r.z+=(r.x+1)*mix(-0.577, 0.577, vertex)
    q = ti.abs(r); return max(q.y-h,max(q.z*0.866025+r.x*0.5,-r.x)-0.5*rt)< 0
@ti.func
def make(func: ti.template(), p1, p2, p3, p4, p5, p6, pos, dir, up, color, mat, mode):
    max_r = 2 * int(max(p3,max(p1, p2))); dir = normalize(dir); up = normalize(cross(cross(dir, up), dir))
    for i,j,k in ti.ndrange((-max_r,max_r),(-max_r,max_r),(-max_r,max_r)): 
        xyz = proj_plane(vec3(0.0,0.0,0.0), dir, up, vec3(i,j,k))
        if func(p1,p2,p3,p4,p5,p6,xyz):
            if mode == 0: scene.set_voxel(pos + vec3(i,j,k), mat, color, 0) # additive
            if mode == 1: scene.set_voxel(pos + vec3(i,j,k), 0, color, 0) # subtractive
            if mode == 2 and scene.get_voxel(pos + vec3(i,j,k))[0] > 0: scene.set_voxel(pos + vec3(i,j,k), mat, color,0 )
@ti.kernel
def duck(x:ti.template()):
    make(elli,32.0,21.8,30.4,0.0,0.0,0.0,vec3(5,-20,-17)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,248,57),1,0)
    make(elli,18.1,18.1,18.1,0.0,0.0,0.0,vec3(6,10,-27)+x,vec3(0.0,1.0,0.0),vec3(1.0,-0.0,-0.0),rgb(255,245,56),1,0)
    make(elli,18.1,10.3,18.1,0.0,0.0,0.0,vec3(8,-16,7)+x,vec3(-0.0,0.4,-0.9),vec3(1.0,-0.0,-0.0),rgb(255,245,56),1,0)
    make(elli,7.6,3.6,6.4,0.0,0.0,0.0,vec3(6,13,-45)+x,vec3(-0.0,0.8,0.6),vec3(1.0,-0.1,0.1),rgb(255,128,55),1,0)
    make(elli,7.6,3.6,6.4,0.0,0.0,0.0,vec3(6,9,-42)+x,vec3(0.0,0.9,-0.4),vec3(1.0,-0.0,0.1),rgb(255,128,55),1,0)
    make(elli,18.1,9.1,18.1,0.0,0.0,0.0,vec3(-13,-22,-15)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,245,56),1,0)
    make(elli,18.1,8.4,18.1,0.0,0.0,0.0,vec3(26,-22,-16)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,245,56),1,0)
    make(elli,2.0,2.4,2.4,0.0,0.0,0.0,vec3(15,17,-40)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,0),1,0)
    make(elli,2.0,2.4,2.4,0.0,0.0,0.0,vec3(-3,17,-39)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,0),1,0)
@ti.kernel
def boat(x:ti.template()):
    make(cyli,6.1,2.1,10.5,0.1,0.0,0.0,vec3(-62,-39,1)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,255,255),1,0)
    make(box,3.2,2.9,3.0,0.1,0.0,0.0,vec3(-62,-36,4)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,255,255),1,0)
    make(cyli,1.2,2.4,1.5,0.1,0.0,0.0,vec3(-62,-31,5)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(255,36,11),1,0)
    make(cyli,7.2,2.6,12.4,0.1,0.0,0.0,vec3(-62,-40,1)+x,vec3(0.0,1.0,0.0),vec3(1.0,0.0,0.0),rgb(0,0,128),1,0)

p = [0.99]

@ti.kernel
def sea(prob:ti.f32):# i: left/right wing,  j: head/tail
    for i, h, j in ti.ndrange((-64, 64), (-64, -40), (-64, 64)):
        scene.set_voxel(vec3(i, h, j), 1, rgb(85+2*h,205+2*h,255)) # sea
        # if h > -50:
        #     scene.set_voxel(vec3(i, h+1*ti.sin(0.2* float(i))*ti.sin(0.2* float(j)), j), 1, rgb(85+2*h,205+2*h,255)) # sea

    for i, h, j in ti.ndrange((-15, 62), (-40, -38), (-38, 64)):
        if j < 0:
            t = (vec2(i, j) - vec2(20,-2) )
            r = 34
            if t.dot(t) < r**2 and ti.random(float) > 0.9:
                scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
        elif ti.random(float) > prob: #- 0.003 * abs(i-20):
            scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave

    for i, h, j in ti.ndrange((-51, -33), (-40, -39), (-12, 64)):
        if j < 10:
            if j < 1:
                s = 7.2 / 12.4
                t = vec2((i-(-42)) *s, j-1)
                r = 10.
                if ti.random(float) > 0.8 and t.dot(t) < r**2:  
                    scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
            elif ti.random(float) > 0.8:  
                scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave
        elif ti.random(float) > 0.85 - 0.005 * abs(i+42) + 0.0015 * (j+13):
            scene.set_voxel(vec3(i, h, j), 2, rgb(255,255,255)) # wave

# direct_light_dir = [-1,1,-0.5]
dir_x = [-1.];dir_y = [1.];dir_z = [-0.5]
def relight():
    scene.set_directional_light([dir_x[0], dir_y[0], dir_z[0]], 0.0, (1, 1, 1))
def create_scene():
    scene.set_directional_light([dir_x[0], dir_y[0], dir_z[0]], 0.0, (1, 1, 1))
    scene.force_reset_scene();duck(vec3(15.,-12.,15));boat(vec3(20.,0.,0.));sea(p[0])

create_scene()
scene.add_slider("prob", p, 0., 1.)
scene.add_slider("direct light x",dir_x, -2., 2. )
scene.add_slider("direct light y",dir_y, -2., 5. )
scene.add_slider("direct light z",dir_z, -2., 2. )

scene.add_callback_button("re-light", relight, ())
scene.add_callback_button("re-wave", sea, (p[0],))
scene.add_callback_button("re-render", create_scene, ())
scene.finish()