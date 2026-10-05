import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up canvas with aspect ratio matching SonicShield reference (tall 3:4 portrait)
fig, ax = plt.subplots(figsize=(8.5, 12), dpi=300)
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Coordinate system: [0, 100] x [0, 100]
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

def draw_box(x, y, w, h, bg_color, border_color='none', text='', subtext='', text_color='white', title_fontsize=13, sub_fontsize=9.5):
    rect = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor=border_color, facecolor=bg_color, zorder=2)
    ax.add_patch(rect)
    
    if text and subtext:
        ax.text(x + w/2, y + h*0.62, text, color=text_color, fontsize=title_fontsize, fontweight='bold',
                ha='center', va='center', zorder=3, fontfamily='sans-serif')
        ax.text(x + w/2, y + h*0.32, subtext, color=text_color, fontsize=sub_fontsize,
                ha='center', va='center', zorder=3, fontfamily='sans-serif')
    elif text:
        ax.text(x + w/2, y + h/2, text, color=text_color, fontsize=title_fontsize, fontweight='bold',
                ha='center', va='center', zorder=3, fontfamily='sans-serif')

def draw_arrow(x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color='black', lw=1.2, mutation_scale=12),
                zorder=1)
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(mid_x + 1.5, mid_y, label, fontsize=8.5, color='black', va='center', fontfamily='sans-serif', zorder=4)

# 1. TOP BAR: Single Breath Input (Bright Sky Blue #0099ff)
draw_box(x=8, y=92, w=84, h=6, bg_color='#0298e8', text='Single Breath Input (Aerosol + Gas Matrix)', title_fontsize=14)

# Vertical drop from Top Bar
draw_arrow(50, 92, 50, 84)
# Horizontal split line
ax.plot([18, 82], [84, 84], color='black', lw=1.2, zorder=1)

# Down to Left Blue Box and Right Green Box
draw_arrow(18, 84, 18, 77)
draw_arrow(82, 84, 82, 77)

# 2. LEFT: 50ms Circular Buffer equivalent -> Micro-Wicking Aerosol Trap (#0055ff Blue)
draw_box(x=4, y=70, w=28, h=7, bg_color='#0055ff',
         text='AEROSOL COLLECTION TRAP', subtext='(Concentrates non-volatile microdroplets)',
         title_fontsize=9.5, sub_fontsize=7.5)

# 3. RIGHT: Speech-Only VAD equivalent -> Breath-Only Flow Gating Trigger (#008800 Green)
draw_box(x=68, y=70, w=28, h=7, bg_color='#008800',
         text='BREATH FLOW GATING TRIGGER', subtext='(Wakes up on valid deep-lung breath)',
         title_fontsize=9, sub_fontsize=7.5)

# Arrows from dual stage down to Crimson Core
draw_arrow(18, 70, 18, 59, label='(Impaction onto\nSPCE strip)')
draw_arrow(82, 70, 82, 59, label='(Wakes up on\nvalid exhalation)')

# 4. WIDE CRIMSON BANNER: Dual Output DCCRN equivalent -> Dual-Domain Transduction Core (#990024)
draw_box(x=4, y=53, w=92, h=6, bg_color='#990024',
         text='DUAL-DOMAIN TRANSDUCTION CORE (SPCE + BME688)',
         title_fontsize=13)

# Sub-labels on Crimson Bar
ax.text(18, 50.5, '[Electrochemical Faradaic Output]', color='#990024', fontsize=9.5, fontweight='bold', ha='center', va='top')
ax.text(82, 50.5, '[Matrix & VOC Verification]', color='#990024', fontsize=9.5, fontweight='bold', ha='center', va='top')

# Arrows from Crimson Bar down to Green Filter
draw_arrow(22, 48, 22, 36)
ax.plot([22, 60], [36, 36], color='black', lw=1.2, zorder=1)
draw_arrow(60, 36, 60, 36)
ax.text(24, 42, '(Faradaic Redox\nSignal Stream)', fontsize=8.5, color='black', va='center')

draw_arrow(82, 48, 82, 38, label='(Environmental\nReference)')

# 5. OLIVE GREEN BOX: Always-on NLMS Filter equivalent -> Always-on 3-Tier ML Engine (#449e1e)
draw_box(x=60, y=32, w=36, h=6, bg_color='#449e1e',
         text='ALWAYS-ON 3-TIER ML ENGINE',
         title_fontsize=11)

# Arrow from Filter down to Final Output
draw_arrow(78, 32, 78, 21)
ax.plot([78, 50], [21, 21], color='black', lw=1.2, zorder=1)
draw_arrow(50, 21, 50, 16)

# 6. FINAL WHITE BOX: Final Output
draw_box(x=35, y=9, w=30, h=7, bg_color='white', border_color='black',
         text='FINAL SCREENING OUTPUT', subtext='(POSITIVE | NEGATIVE | INCONCLUSIVE)',
         text_color='black', title_fontsize=11, sub_fontsize=8)

plt.tight_layout()
output_path = '/Users/yogipatel/Desktop/Code/PS/AeroTrace_Block_Diagram_SonicShield_Style.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Diagram saved to {output_path}")
