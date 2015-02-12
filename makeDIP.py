import os

def makeName(PinCount):
    name = "PDIP-"+str(PinCount)
    return name
    
def makePins(PinCount):
    pre = "  (pad "
    shape = " thru_hole circle (at "
    last = ") (size 1.6 1.6) (drill 0.8) (layers *.Cu *.Mask F.SilkS))\n"
    offset = 0
    xLoc = round((2.54*3)/2, 3)
    yMax = round((2.54*PinCount)/4, 3)
    if (PinCount/2)%2==0:
        yMax = yMax - 1.27
    
    pins = []
    
    pins.append(pre+"1 thru_hole rect (at ")
    pins[0] = pins[0]+"-"+str(xLoc)+" "+str(round(-1*yMax,3)) +last  
    
    for i in range(2, PinCount+1):
    
        pins.append(pre+str(i)+shape)
        if i<=PinCount/2:
            pins[i-1] = pins[i-1]+"-"+str(xLoc)+" "+str(round(-1*(yMax-(2.54*(i-1))),3))
        else:
            pins[i-1] = pins[i-1]+str(xLoc)+" "+str(round(-1*(-yMax+(2.54*(i-1-PinCount/2))),3))
        
        pins[i-1] = pins[i-1] + last

    return pins

def makeOutline(PinCount):
    
    xArc = str(7.11/4)
    xCorner = str(5)
    yCorner = str(round(2.54*(PinCount/4),3))
    
    lines = []
    lines.append('  (fp_arc (start 0 -')
    lines[0] = lines[0] + yCorner + ') (end ' + xArc +' -'
    lines[0] = lines[0] + str(yCorner)
    lines[0] = lines[0] + ') (angle 180) (layer F.SilkS) (width 0.15))\n'
    lines.append('  (fp_line (start -' + xArc + ' -' + yCorner + ') (end -' + 
                 xCorner + ' -' + yCorner + ') (layer F.SilkS) (width 0.15))\n')
    lines.append('  (fp_line (start -' + xCorner + ' -' + yCorner + ') (end -' + 
                 xCorner + ' ' + yCorner + ') (layer F.SilkS) (width 0.15))\n')
    lines.append('  (fp_line (start -' + xCorner + ' ' + yCorner + ') (end ' + 
                 xCorner + ' ' + yCorner + ') (layer F.SilkS) (width 0.15))\n')
    lines.append('  (fp_line (start ' + xCorner + ' ' + yCorner + ') (end ' + 
                 xCorner + ' -' + yCorner + ') (layer F.SilkS) (width 0.15))\n')
    lines.append('  (fp_line (start ' + xCorner + ' -' + yCorner + ') (end ' + 
                 xArc + ' -' + yCorner + ') (layer F.SilkS) (width 0.15))\n')
    
    return lines
    
def makeRef(PinCount):
    name = makeName(PinCount)
    ref = []
    ref.append('  (fp_text reference '+name+' (at 0 ')
    ref[0] = ref[0]+'-'+str(round(1.27*PinCount/2 + 1.27,3))+') (layer Dwgs.User)\n'
    ref.append('    (effects (font (size 1 1) (thickness 0.15)))\n')
    ref.append('  )\n')
    
    return ref

def makeVal(PinCount):
    name = makeName(PinCount)
    val = []
    val.append('  (fp_text value VAL** (at 0 ')
    val[0] = val[0]+str(round(1.27*PinCount/2 + 1.27,3))+') (layer F.SilkS)\n'
    val.append('    (effects (font (size 1 1) (thickness 0.15)))\n')
    val.append('  )\n')
    
    return val
    
def makeFootprint(PinCount):
    file = []
    name = makeName(PinCount)
    ref = makeRef(PinCount)
    val = makeVal(PinCount)
    pins = makePins(PinCount)
    lines = makeOutline(PinCount)
    
    file.append('(module '+name+' (layer F.Cu)\n')
    file.append('  (descr "'+name+'")\n')
    file.append('  (tags "pdip")\n')
    
    for l in ref:
        file.append(l)
        
    for l in val:
        file.append(l)
        
    for l in lines:
        file.append(l)
        
    for l in pins:
        file.append(l)
        
    file.append(')\n')
     
    return file
    
def makeFile(PinCount):
    file = makeFootprint(PinCount)
    fileName = makeName(PinCount)+'.kicad_mod'
    with open(fileName, mode='w') as f:
        f.writelines(file)
