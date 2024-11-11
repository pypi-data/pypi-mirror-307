import numpy as np
import pandas as pd
from shapely.geometry import Point,Polygon


from . import entropy
from . import topo



def initialize(bbox,df,x_mul,y_mul,bbox_cor,angleRotate):
    d = {}
    i = 0
    x_min = bbox_cor[1]
    y_min = bbox_cor[2]
    # gdf to df
    for idxP in range(df.shape[0]):
        try:
            d[i] = {'geometry': df['geometry'][idxP].exterior.coords.xy, 'cent': df['cent'][idxP].coords.xy}
            i+=1
        except:
            i = i
    df = pd.DataFrame.from_dict(d, "index")
    # Convert lat/long to x/y 2D empty domain
    bb = np.zeros(np.shape(bbox))
    xxx = []
    yyy = []
    for i in range(np.shape(bbox)[0]):
        bb[i][0] = int(np.round((bbox[i][0] - x_min)*x_mul))
        bb[i][1] = int(np.round((bbox[i][1] - y_min)*y_mul))
        xxx.append(int(np.round((bbox[i][0] - x_min)*x_mul)))
        yyy.append(int(np.round((bbox[i][1] - y_min)*y_mul)))
        
    domain1 = np.zeros([np.max(xxx)-np.min(xxx),np.max(yyy)-np.min(yyy)]) # domain that contains the topography

    _,_,domain = topo.rotateS(0,0,domain1,angleRotate) # domain that contains topography after rotation

    return(domain1,domain,df,np.min(xxx),np.min(yyy)) # return the 



def process_building(lineO,lineL,domain1,domain,idxP,gdf,bHeightL,bHeightH,x_mul,y_mul,x_start,y_start,bbox_cor,bldH,area,areaH,res,angleRotate):
    # poly.bounds
    nx = []
    ny = []
    xy = []
    Pol = []

    # Collect and project points in the geometry
    for i in range(np.shape(gdf['geometry'][idxP])[1]):
        xb = int(np.round((gdf['geometry'][idxP][0][i] - bbox_cor[1])*x_mul))-x_start
        yb = int(np.round((gdf['geometry'][idxP][1][i] - bbox_cor[2])*y_mul))-y_start

        xx,yy,_ = topo.rotateS(xb,yb,domain1,angleRotate)


        nx.append(xx+x_start)
        ny.append(yy+y_start)
        xy.append([xx+x_start,yy+y_start])
        Pol.append((xx,yy))
        
    [lineO,lineL] = entropy.count_edge(xy,lineO,lineL,res) # working

    pol = Polygon(Pol)
    area.append(pol.area)
    AA = True
        
    # transfer all nan to zeros first

    bHeightL[np.isnan(bHeightL)] = 0
    bHeightH[np.isnan(bHeightH)] = 0

    if bHeightH[idxP]==0: # consider the actual height first
        if bHeightL[idxP]==0: 
            HH = bldH  # no bHeightL and bHeightH
            AA = False

        else:
            #print('L')
            HH = float(bHeightL[idxP])
            areaH.append(pol.area) # count surface of buildings that have real heights
    else:
        #print('H')
        HH = float(bHeightH[idxP])
        areaH.append(pol.area)
    
    domain = construct(domain,HH,nx,ny,x_start,y_start,pol)
    
    
    return(domain,areaH,area)




def construct(domain,HH,nx,ny,x_start,y_start,pol):
    # Construct edge
    xmin = np.min(nx) - x_start
    xmax = np.max(nx) - x_start
    ymin = np.min(ny) - y_start
    ymax = np.max(ny) - y_start
    #for ii in range(np.size(nx)): # don't fill the vertices for better looking
    #    try:
    #        domain[nx[ii]-x_start,ny[ii]-y_start] = HH # Fill the outline with building height
    #    except:
    #        continue

    # Construct interior by filling grids with building height
    for x in range (xmin,xmax):
        for y in range(ymin,ymax):
            p = Point(x,y)
            if p.within(pol) or p.intersects(pol):
                try:
                    domain[x,y] = HH  # Fill inside with building height
                except:
                    continue   
    return(domain)