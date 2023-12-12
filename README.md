# Topology Editor
User-friendly editor to load, edit, and save topology
참고:
https://www.notion.so/Web-Editor-0eb40aebe3644e36aa41faec84ca6cf8#b823b729a74e4ca3b279f36c589182ff

기능:
Topology 로드/저장
Vertex 추가(클릭) / 삭제(해당 Vertex 우클릭) / 여려개 추가 (우클릭 후 드래기)
Edge 1개 / 여러개 추가

# How to Use 
1. topology_web_editor/frontend/style.css
    - markerContainer 의 width: map.png 가로 픽셀 수로 세팅
    - mapImage 의 width: map.png 가로 픽셀 수로 세팅
2. topology_web_editor/frontend/map.png
    - navigation map 파일 추가
3. topology_web_editor/frontend/editor.html
    - visualizedEdges(canvas)의 width, height map.png의 가로, 세로 픽셀 수로 세팅
4. chmod +x topology_web_editor/run.sh
5. ./run.sh
6. map.yaml , topology.yaml 경로 순서대로 추가
    - “Tab” key로 default 값 입력 가능
        - “/opt/floatic/config/env/map/navigation/map.yaml”
        - “/opt/floatic/config/env/map/navigation/topology.yaml”
7. 수정 후 output 파일 경로 입력 후 Save
