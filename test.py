import pyglet
jawa = pyglet.image.load('Jawa.png')
jawa_seq = pyglet.image.ImageGrid(jawa,4,3)
jawa_ani = []
for i in range(4):
    dur = 1
    print range(3*i,3*i+2)
    jawa_ani.append(pyglet.image.Animation.from_image_sequence(jawa_seq[3*i:3*i+2],dur))
