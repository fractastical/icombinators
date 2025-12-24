/**
 * Generate visualization figures using browser/D3.js
 * Run this in Node.js with jsdom or in a browser environment
 * 
 * Usage: node generate_figures_browser.js
 */

// This script generates HTML files that can be opened in a browser
// to generate screenshots, or uses headless browser automation

const fs = require('fs');
const path = require('path');

// Graph creation functions (simplified versions)
function createLoopExample() {
    return {
        nodes: [
            {id: 0, type: 'Arrow', x: 200, y: 200},
            {id: 1, type: 'Arrow', x: 400, y: 200},
            {id: 2, type: 'Arrow', x: 300, y: 350}
        ],
        links: [
            {source: 0, target: 1},
            {source: 1, target: 2},
            {source: 2, target: 0}
        ]
    };
}

function createOuroboros() {
    const nodes = [];
    const links = [];
    const n = 5;
    const centerX = 300;
    const centerY = 300;
    const radius = 150;
    
    for (let i = 0; i < n; i++) {
        const angle = (2 * Math.PI * i) / n;
        nodes.push({
            id: i,
            type: i % 2 === 0 ? 'L' : 'A',
            x: centerX + radius * Math.cos(angle),
            y: centerY + radius * Math.sin(angle)
        });
        if (i > 0) {
            links.push({source: i - 1, target: i});
        }
    }
    links.push({source: n - 1, target: 0}); // Close the loop
    
    return {nodes, links};
}

function createHTMLVisualization(graph, title, filename) {
    const nodeColors = {
        'L': '#4ec9b0',
        'A': '#ce9178',
        'FI': '#569cd6',
        'FO': '#dcdcaa',
        'Arrow': '#c586c0',
        'T': '#808080'
    };
    
    const html = `<!DOCTYPE html>
<html>
<head>
    <title>${title}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { margin: 0; background: #000; }
        svg { width: 100%; height: 100vh; }
        .node { cursor: pointer; }
        .link { stroke: #666; stroke-width: 2; fill: none; }
        .node-label { fill: #fff; font-size: 10px; font-family: monospace; text-anchor: middle; }
    </style>
</head>
<body>
    <svg id="graph"></svg>
    <script>
        const graph = ${JSON.stringify(graph)};
        const svg = d3.select("#graph");
        const width = window.innerWidth;
        const height = window.innerHeight;
        svg.attr("width", width).attr("height", height);
        
        const simulation = d3.forceSimulation(graph.nodes)
            .force("link", d3.forceLink(graph.links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(20));
        
        const link = svg.append("g")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link");
        
        const node = svg.append("g")
            .selectAll("circle")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 15)
            .attr("fill", d => {
                const colors = {
                    'L': '#4ec9b0', 'A': '#ce9178', 'FI': '#569cd6',
                    'FO': '#dcdcaa', 'Arrow': '#c586c0', 'T': '#808080'
                };
                return colors[d.type] || '#ffffff';
            })
            .attr("stroke", "#fff")
            .attr("stroke-width", 2);
        
        const label = svg.append("g")
            .selectAll("text")
            .data(graph.nodes)
            .enter().append("text")
            .attr("class", "node-label")
            .text(d => d.type);
        
        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
            
            label
                .attr("x", d => d.x)
                .attr("y", d => d.y + 4);
        });
        
        // Wait for simulation to settle, then save
        setTimeout(() => {
            console.log("Graph rendered. Take screenshot manually or use automation.");
        }, 2000);
    </script>
</body>
</html>`;
    
    fs.writeFileSync(filename, html);
    console.log(`Created ${filename}`);
}

// Generate HTML files
const figuresDir = 'figures_html';
if (!fs.existsSync(figuresDir)) {
    fs.mkdirSync(figuresDir);
}

createHTMLVisualization(createLoopExample(), 'Loop Example', `${figuresDir}/loop_example.html`);
createHTMLVisualization(createOuroboros(), 'Ouroboros', `${figuresDir}/ouroboros.html`);

console.log(`\nHTML files created in ${figuresDir}/`);
console.log('Open in browser and take screenshots, or use headless browser automation.');

