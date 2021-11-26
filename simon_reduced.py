def simon_reduced(qc, l, r, k0, k1, state_size):
    for i in range(state_size):
        qc.ccx(l[(i-1)%state_size],l[(i-8)%state_size],r[i])
        qc.cx(l[(i-2)%state_size],r[i])
        qc.cx(k0[i],r[i])

    for i in range(state_size):
        qc.ccx(r[(i-1)%state_size],r[(i-8)%state_size],l[i])
        qc.cx(r[(i-2)%state_size],l[i])
        qc.cx(k1[i],l[i])
