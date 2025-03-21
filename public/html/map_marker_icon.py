
def map_marker_icon(color, number):

    return f'''
<div style="position: relative; width: 32px; height: 54px; display: flex; flex-direction: column; align-items: center;">
    <!-- Number Box Above Marker with Protruding Effect -->
    <div style="
        position: absolute;
        top: -22px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #1E1E1E;
        color: white;
        padding: 4px 10px;
        font-size: 13px;
        font-weight: bold;
        border-radius: 6px;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.4);
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        {number}
    </div>

    <!-- Marker Shape with Inner Layer Effect -->
    <svg width="32" height="54" viewBox="0 0 32 54" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="rgba(0,0,0,0.4)" />
            </filter>
        </defs>
        <path d="M16,0 C24,-2 32,10 32,20 C32,30 16,48 16,54 C16,48 0,30 0,20 C0,10 8,-2 16,0 Z"
            fill="{color}"
            stroke="none"
            filter="url(#shadow)" />

        <!-- Inner Circle for Extra Layering -->
        <circle cx="16" cy="20" r="7"
            fill="rgba(255,255,255,0.9)"
            stroke="{color}"
            stroke-width="2" />
    </svg>
</div>
'''


def map_star_marker(color, number):

    return f'''
        <div style="position: relative; width: 50px; height: 50px; display: flex; flex-direction: column; align-items: center;">
    <!-- Number Box Above Star with More Protruding Effect -->
    <div style="
        position: absolute;
        top: -22px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #1E1E1E;
        color: white;
        padding: 6px 12px;
        font-size: 14px;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        {number}
    </div>

    <!-- Minimalist Star Shape -->
    <svg width="50" height="50" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
        <polygon points="25,5 32,18 46,20 35,30 38,45 25,38 12,45 15,30 4,20 18,18"
            fill="{color}"
            stroke="none" />
    </svg>
</div>
'''


def map_x_marker(color, number):

    return f'''

        <div style="position: relative; width: 50px; height: 50px; display: flex; flex-direction: column; align-items: center;">
            <!-- Number Box Above X with More Protruding Effect -->
            <div style="
                position: absolute;
                top: -22px;
                left: 50%;
                transform: translateX(-50%);
                background-color: #1E1E1E;
                color: white;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
                z-index: 10;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                {number}
            </div>

            <!-- Minimalist X Shape -->
            <svg width="50" height="50" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
                <line x1="10" y1="10" x2="40" y2="40" stroke="{color}" stroke-width="6" stroke-linecap="round" />
                <line x1="40" y1="10" x2="10" y2="40" stroke="{color}" stroke-width="6" stroke-linecap="round" />
            </svg>
        </div>

'''


def map_flag_marker(color, number):

    return f'''
        <div style="position: relative; width: 50px; height: 80px; display: flex; flex-direction: column; align-items: center;">
            <!-- Number Box Above Flag with More Protruding Effect -->
            <div style="
                position: absolute;
                top: -22px;
                left: 50%;
                transform: translateX(-50%);
                background-color: #1E1E1E;
                color: white;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
                z-index: 10;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                {number}
            </div>

            <!-- Refined Flag Shape with a Single Axis -->
            <svg width="50" height="80" viewBox="0 0 50 80" xmlns="http://www.w3.org/2000/svg">
                <rect x="10" y="10" width="6" height="60" fill="#333" />
                <rect x="16" y="10" width="25" height="20" fill="{color}" stroke="none" />
            </svg>
        </div>
'''
