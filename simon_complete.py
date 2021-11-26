def simon4(qc, r, l, k0, k1, k2, k3):
    state_size = 16
    rounds = 7
    rc = [1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,0,0,1,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,
        1,0,0,0,0,1,1,1,0,0,1,1,0]

    for j in range(rounds):
        
        for i in range(state_size):
            qc.ccx(l[(i-1)%state_size],l[(i-8)%state_size],r[i])
            qc.cx(l[(i-2)%state_size],r[i])
            qc.cx(k0[i],r[i])
        
        for i in range(state_size):
            qc.ccx(r[(i-1)%state_size],r[(i-8)%state_size],l[i])
            qc.cx(r[(i-2)%state_size],l[i])
            qc.cx(k1[i],l[i])
        
        for i in range(state_size):
            qc.ccx(l[(i-1)%state_size],l[(i-8)%state_size],r[i])
            qc.cx(l[(i-2)%state_size],r[i])
            qc.cx(k2[i],r[i])
        
        for i in range(state_size):
            qc.ccx(r[(i-1)%state_size],r[(i-8)%state_size],l[i])
            qc.cx(r[(i-2)%state_size],l[i])
            qc.cx(k3[i],l[i])

    
        for i in range(state_size): 
            qc.cx(k1[i],k0[i])
            qc.cx(k1[(i+1)%state_size],k0[i])
            qc.cx(k3[(i+3)%state_size],k0[i])
            qc.cx(k3[(i+4)%state_size],k0[i])
        for i in range(2,state_size):
            qc.x(k0[i])
        if(rc[(j*4)%62]==1):
            qc.x(k0[0])
            
        
        for i in range(state_size): 
            qc.cx(k2[i],k1[i])
            qc.cx(k2[(i+1)%state_size],k1[i])
            qc.cx(k0[(i+3)%state_size],k1[i])
            qc.cx(k0[(i+4)%state_size],k1[i])
        for i in range(2,state_size):
            qc.x(k1[i])
        if(rc[((j*4)+1)%62]==1):
            qc.x(k1[0])
        
        for i in range(state_size): 
            qc.cx(k3[i],k2[i])
            qc.cx(k3[(i+1)%state_size],k2[i])
            qc.cx(k1[(i+3)%state_size],k2[i])
            qc.cx(k1[(i+4)%state_size],k2[i])
        for i in range(2,state_size):
            qc.x(k2[i])
        if(rc[((j*4)+2)%62]==1):
            qc.x(k2[0])
        
        for i in range(state_size): 
            qc.cx(k0[i],k3[i])
            qc.cx(k0[(i+1)%state_size],k3[i])
            qc.cx(k2[(i+3)%state_size],k3[i])
            qc.cx(k2[(i+4)%state_size],k3[i])
        for i in range(2,state_size):
            qc.x(k3[i])
        if(rc[((j*4)+3)%62]==1):
            qc.x(k3[0])
            
    
    for i in range(state_size):
        qc.ccx(l[(i-1)%state_size],l[(i-8)%state_size],r[i])
        qc.cx(l[(i-2)%state_size],r[i])
        qc.cx(k0[i],r[i])
        
    for i in range(state_size):
        qc.ccx(r[(i-1)%state_size],r[(i-8)%state_size],l[i])
        qc.cx(r[(i-2)%state_size],l[i])
        qc.cx(k1[i],l[i])
        
    for i in range(state_size):
        qc.ccx(l[(i-1)%state_size],l[(i-8)%state_size],r[i])
        qc.cx(l[(i-2)%state_size],r[i])
        qc.cx(k2[i],r[i])
        
    for i in range(state_size):
        qc.ccx(r[(i-1)%state_size],r[(i-8)%state_size],l[i])
        qc.cx(r[(i-2)%state_size],l[i])
        qc.cx(k3[i],l[i])