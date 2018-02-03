print('loading main.py')

from browser import document, alert, window, timer
from math import sin, cos, tan, radians
from random import choice

result = window.gebi('result')
start = window.gebi('start')

win = window.gebi('win')
challenges = window.gebi('challenges')

display = window.gebi('display')
map_ = window.gebi('map')
cloud_canvas = window.gebi('clouds_canvas')

cloud_ctx = cloud_canvas.getContext('2d')
ctx = display.getContext('2d')
map_ctx = map_.getContext('2d')

class Turtle(object):
  angles = [62.64,-62.64,-117.36,117.36]

  def __init__(self):
    self.x = 0
    self.y = 0
    self.angle = 0

    self.disp_x = 0
    self.disp_y = 0

    self.origin_x, self.origin_y = window.data['player_origin']
    self.collision_map = window.data['collisions']

  def collision(self):
    x_pos = round(self.origin_x + self.disp_x)
    y_pos = round(self.origin_y + self.disp_y)

    try:
      if self.collision_map[y_pos][x_pos]:
        return 1
    except IndexError:
      return 1

    return 0

  def forward(self,dist):
    self.x += sin(radians(self.angles[self.angle]))*dist*(display.height/(2*iso_scale))/(cos(radians(62.64)))
    self.y += cos(radians(self.angles[self.angle]))*dist*(display.height/(2*iso_scale))/(cos(radians(62.64)))

    if self.angle == 0:
      self.disp_x += dist
    elif self.angle == 1:
      self.disp_y += dist
    elif self.angle == 2:
      self.disp_x -= dist
    elif self.angle == 3:
      self.disp_y -= dist
    else:
      print('Issue in displacement tracking!')

  def backward(self,dist):
    self.x -= sin(radians(self.angles[self.angle]))*dist*(display.height/(2*iso_scale))/(cos(radians(62.64)))
    self.y -= cos(radians(self.angles[self.angle]))*dist*(display.height/(2*iso_scale))/(cos(radians(62.64)))

    if self.angle == 0:
      self.disp_x -= dist
    elif self.angle == 1:
      self.disp_y -= dist
    elif self.angle == 2:
      self.disp_x += dist
    elif self.angle == 3:
      self.disp_y += dist
    else:
      print('Issue in displacement tracking!')

  def left(self,rot):
    tval = self.angle + int(rot)
    self.angle = tval % 4

  def right(self,rot):
    tval = self.angle - int(rot)
    self.angle = tval % 4

class Cloud(object):
  x = 0
  y = 0
  speed = 0

  src = window.gebi(choice(['cloud1', 'cloud2']))

turtle = Turtle()

cmd = {
  'FORWARD' : turtle.forward,
  'BACKWARD' : turtle.backward,
  'LEFT' : turtle.left,
  'RIGHT' : turtle.right,
  'FOR ' : None,
  'ENDFOR' : None
}

run_buffer = []
used_commands = []
runtime = None

def run():
  global runtime
  global run_buffer
  global used_commands

  variables = {}

  window.gebi('error').style.width = '0vw'
  window.gebi('error').style.opacity = 0

  try:
    window.clearInterval(runtime)
  except:
    pass

  display.width = display.width
  turtle.x = display.width / 2
  turtle.y = display.height / 2

  turtle.disp_x = 0
  turtle.disp_y = 0

  turtle.angle = 0

  ctx.beginPath()
  ctx.lineWidth = 3
  ctx.moveTo(turtle.x + dis_center_x,turtle.y + dis_center_y)
  ctx.stroke()

  lines = window.editor.getValue().split('\n')
  lines = list(filter(lambda x: bool(x), lines))

  used_commands = []

  run_buffer = []
  for_buffer = []
  current_buffer = run_buffer

  for line in lines:
    line = line.strip()
    if '=' in line:
      pre, post = line.split('=')

      pre = pre.strip()

      if pre[0] in '0123456789':
        window.gebi('error').style.width = '42vw'
        window.gebi('error').style.opacity = 1
        window.gebi('error').innerHTML =  'Error in line "{}": Declarations cannot begin with numericals'.format(line)
        window.hide_error()
        return

      post = post.strip()

      for char in pre:
        if char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
          window.gebi('error').style.width = '42vw'
          window.gebi('error').style.opacity = 1
          window.gebi('error').innerHTML =  'Error in line "{}": "{}" not allowed in variable declarations'.format(line, char)
          window.hide_error()
          return

      variables[pre] = post

    else:
      for command, action in cmd.items():
        if line.startswith(command):
          used_commands.append(command)

          if command in ['FORWARD', 'BACKWARD']:
            try:
              arg = int(line.split(' ',1)[1])
            except ValueError:
              try:
                arg = int(variables[line.split(' ',1)[1]])
              except ValueError:
                window.gebi('error').style.width = '42vw'
                window.gebi('error').style.opacity = 1
                window.gebi('error').innerHTML =  'Error in line "{}": {} only accepts integer values (whole numbers)'.format(line, command)
                window.hide_error()
                return

              except KeyError:
                window.gebi('error').style.width = '42vw'
                window.gebi('error').style.opacity = 1
                window.gebi('error').innerHTML =  'Error in line "{}": variable "{}" not defined'.format(line, line.split(' ')[1])
                window.hide_error()
                return

            for i in range(5*arg):
              current_buffer.append(command + ' 0.2')

          elif command in ['LEFT','RIGHT']:
            current_buffer.append(command + ' 1')

          elif command in ['FOR ']:
            try:
              arg = int(line.split(' ',1)[1])
            except ValueError:
              window.gebi('error').style.width = '42vw'
              window.gebi('error').style.opacity = 1
              window.gebi('error').innerHTML =  'Error in line "{}": {} only accepts integer values (whole numbers)'.format(line, command)
              window.hide_error()
              return

            if len(for_buffer) > 0:
              for_buffer.append([arg])
              current_buffer = for_buffer[-1]
            else:
              for_buffer.append(arg)
              current_buffer = for_buffer

          elif command in ['ENDFOR']:
            if current_buffer == for_buffer[-1]:
              cur = for_buffer.pop(-1)
              counts = cur.pop(0)
              apval = cur*counts
              try:
                for item in apval:
                  for_buffer[-1].append(item)
                current_buffer = for_buffer[-1]
              except:
                for item in apval:
                  for_buffer.append(item)
                current_buffer = for_buffer

            elif current_buffer == for_buffer:
              counts = for_buffer.pop(0)
              apval = for_buffer*counts
              for item in apval:
                run_buffer.append(item)

              current_buffer = run_buffer

          break
      else:
        window.gebi('error').style.width = '42vw'
        window.gebi('error').style.opacity = 1
        window.gebi('error').innerHTML =  'Error in line "{}": Unrecognised command-word'.format(line)
        window.hide_error()
        break

  runtime = window.setInterval(run_action,35)

def run_action():
  if len(run_buffer) == 0:
    print('exec finished')
    window.clearInterval(runtime)
    post_run()
    return
  a = run_buffer.pop(0)

  arg = float(a.split(' ',1)[1])
  cmd[a.split(' ')[0]](arg)

  display.width = display.width
  imgs = ['front_r', 'front', 'back_l', 'back']

  ctx.drawImage(window.gebi(imgs[turtle.angle]), turtle.x - 50, turtle.y - 100, 100, 100)

  if turtle.collision():
    window.clearInterval(runtime)
    window.gebi('error').style.width = '42vw'
    window.gebi('error').style.opacity = 1
    window.gebi('error').innerHTML = 'Rodrick can\'t move there!'
    window.hide_error()

def post_run():

  if [int(turtle.disp_x), int(turtle.disp_y)] == window.data['displacement']:
    completed = []
    challenge_text = []

    for typ, target in dict(window.data['targets']).items():
      if typ == 'LINES':
        if len(used_commands) <= target:
          challenge_text.append('Use {} or less lines ⭐'.format(target))
          completed.append([typ, target])
        else:
          challenge_text.append('Use {} or less lines'.format(target))

      elif typ == '!USE':
        for command in target:
          if command in used_commands:
            challenge_text.append('Don\'t use {} anywhere in your code'.format(', '.join(target)))
            break
        else:
          challenge_text.append('Don\'t use {} anywhere in your code ⭐'.format(', '.join(target)))
          completed.append([typ, target])

      elif typ == 'USE':
        for command in target:
          if command in used_commands:
            challenge_text.append('Apply a {} somewhere in your code ⭐'.format(', '.join(target)))
            completed.append([typ, target])
            break
        else:
          challenge_text.append('Apply a {} somewhere in your code'.format(', '.join(target)))

    window.on_win()
    challenges.innerHTML = '<br>'.join(challenge_text) + '<br><hr>'

keysdown = []

def keysDown(event):
  keysdown.append(event.keyCode)

  if 13 in keysdown and 16 in keysdown:
    event.preventDefault()
    run()

  elif 17 in keysdown and 83 in keysdown:
    event.preventDefault()
    window.save(window.editor.getValue().replace('\n','\\'))

def keysUp(event):
  try:
    keysdown.remove(event.keyCode)
  except:
    pass

clouds = []

for i in range(4):
  c = Cloud()
  c.x = result.width * window.Math.random()
  c.y = result.height * 0.5 * window.Math.random() + result.height * 0.04
  c.speed = 2.2 * window.Math.random() + 1

  clouds.append(c)

def clouds_render():
  cloud_canvas.width = result.width
  cloud_canvas.height = result.height

  cloud_w = cloud_canvas.width / 5.5
  cloud_h = cloud_w / 2

  for cloud in clouds:
    cloud.x -= cloud.speed

    cloud_ctx.drawImage(cloud.src, cloud.x, cloud.y, cloud_w, cloud_h)

    if cloud.x < -cloud_w:
      cloud.x = result.width
      cloud.y = result.height * 0.5 * window.Math.random() + result.height * 0.04
      cloud.speed = 2 * window.Math.random() + 0.5

iso_scale = window.data['gridSize']
median_cell = ()

dis_center_x = 0
dis_center_y = 0

def resize_window(event):
  display.width = result.width
  display.height = result.height

  map_.width = result.width
  map_.height = result.height

  cell_w = (display.height/iso_scale)*tan(radians(62.64))
  cell_h = display.height/iso_scale

  median_cell = (display.width/2,display.height/2)

  ## READING MAP DATA ##

  for i,j,src,c in window.data['map']:
    map_ctx.beginPath()

    if c[0] == 'simpleFill':
      img = window.gebi(src)

      # ANTIALIAS #
      oc = document.createElement('canvas')
      oc2 = document.createElement('canvas')
      octx = oc.getContext('2d')
      octx2 = oc2.getContext('2d')

      oc.width = img.width
      oc.height = img.height

      oc2.width = img.width
      oc2.height = img.height

      octx.drawImage(img, 0, 0, oc.width, oc.height)
      octx2.drawImage(oc, 0, 0, oc.width * 0.5, oc.height * 0.5)

      oc.width = oc.width
      octx.drawImage(oc2, 0, 0, oc.width * 0.5, oc.height * 0.5)

      oc2.width = oc2.width
      octx2.drawImage(oc, 0, 0, oc.width * 0.5, oc.height * 0.5)

      map_ctx.drawImage(
        oc2, 0, 0, oc.width * 0.125, oc.height * 0.125,
        (median_cell[0] + i*cell_w) - c[2][0] * cell_w,
        (median_cell[1] + j*cell_h) - c[2][1] * cell_h,
        c[1][0]*cell_w+c[2][0]*cell_w,
        c[1][1]*cell_h+c[2][1]*cell_h
      )
      map_ctx.fill()

    elif c == 'floor':
      map_ctx.moveTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h - cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w + cell_w/2,median_cell[1] + j*cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h + cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h)

      pattern = ctx.createPattern(window.gebi(src), 'repeat')

      map_ctx.fillStyle = pattern
      map_ctx.fill()

    elif c == 'wall_l':
      map_ctx.moveTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h - cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h - cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h + cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h)

      pattern = map_ctx.createPattern(window.gebi(src), 'repeat')

      map_ctx.fillStyle = pattern
      map_ctx.fill()

      map_ctx.beginPath()

      map_ctx.globalAlpha = 0.5

      map_ctx.moveTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h - cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h - cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h + cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h)

      pattern = map_ctx.createPattern(window.gebi(src), 'repeat')

      map_ctx.fillStyle = '#000000'
      map_ctx.fill()

      map_ctx.globalAlpha = 1

    elif c == 'wall_r':

      map_ctx.moveTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h - cell_h)
      map_ctx.lineTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h - cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w - cell_w/2,median_cell[1] + j*cell_h + cell_h/2)
      map_ctx.lineTo(median_cell[0] + i*cell_w,median_cell[1] + j*cell_h)

      pattern = map_ctx.createPattern(window.gebi(src), 'repeat')

      map_ctx.fillStyle = pattern
      map_ctx.fill()

start.onclick = run

window.onresize = resize_window
window.setInterval(clouds_render,55)

document.onkeydown = keysDown
document.onkeyup = keysUp

def load():
  resize_window(None)
  window.hide_load()

document.onload = load()

print('main.py loaded')
