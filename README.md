# Topology Editor
User-friendly editor to load, edit, and save topology

# How to Use 
1. topology_web_editor/frontend/style.css
    - markerContainer 의 width: map.png 가로 픽셀 수로 세팅
    - mapImage 의 width: map.png 가로 픽셀 수로 세팅
2. topology_web_editor/frontend/map.png
    - navigation map 파일 추가
3. topology_web_editor/frontend/editor.html
    - visualizedEdges(canvas)의 width, height map.png의 가로, 세로 픽셀 수로 세팅
4. topology_web_editor/frontend
    - python3 -m http.server --bind 127.0.0.1 실행
5. topology_web_editor/backend
    - python3 [app.py](http://app.py)
6. map.yaml , topology.yaml 경로 순서대로 추가
    - “Tab” key로 default 값 입력 가능
        - “/opt/floatic/config/env/map/navigation/map.yaml”
        - “/opt/floatic/config/env/map/navigation/topology.yaml”
7. 수정 후 output 파일 경로 입력 후 Save

