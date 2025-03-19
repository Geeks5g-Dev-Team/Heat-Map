
def map_marker_icon(color, number):

    return f"""

        <div style="position: relative; width: 30px; height: 50px;">

            <!-- Number Box Above Marker -->
            <div style="
                position: absolute;
                top: -20px;
                left: 50%;
                transform: translateX(-50%);
                background-color: #212529;
                color: white;
                padding: 3px 8px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 4px;
                box-shadow: 0px 2px 4px rgba(0,0,0,0.3);
                z-index: 10;
            ">
                {number}
            </div>

            <!-- Marker Shape -->
            <svg width="30" height="50" viewBox="0 0 30 50" xmlns="http://www.w3.org/2000/svg">
                <path d="M15,0 C22,-2 30,8 30,18 C30,28 15,45 15,50 C15,45 0,28 0,18 C0,8 8,-2 15,0 Z"
                    fill="{color}"
                    stroke="none" />

                <!-- Inner Circle -->
                <circle cx="15" cy="18" r="6"
                    fill="rgba(255,255,255,0.8)"
                    stroke="{color}"
                    stroke-width="1" />
            </svg>
        </div>
"""
