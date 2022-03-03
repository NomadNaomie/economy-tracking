/*
* This pie chart shows the percentage of diamonds earned at each shop
* in Order to make it readable, some shops will need to be grouped into other
*/

//Dimensions and bounds of the Pie Chart
const pie_width = 700,
    pie_height = 850,
    pie_margin = 40;

//The radius will be the min value of the width or height minus the offset
const radius = Math.min(pie_width, pie_height) / 2 - pie_margin

//Find the div with id pie and append an SVG with given dimensions
const pie_svg = d3.select("#pie")
  .append("svg")
    .attr("width", pie_width)
    .attr("height", pie_height)
  .append("g")
    .attr("transform", `translate(${pie_width / 2}, ${pie_height / 2})`);

//Data from ledger, commented out shops are moved into "other"
const data = {
  "Direct": 1042,
  "G-Train": 1024,
  "Big Eyes Pass N Gas": 309,
  "Padllama Co.": 290,
  "Evil Emporium": 391,
  "Shulker Box": 527,
  "Swaggon": 303,
  "Horse Head Farms": 526,
  "iCandy": 179,
  "Octagon": 186,
  "Other": 1161+125+139}

//var for the colour scheme for pie slices
var color = d3.scaleOrdinal()
.range(d3.schemeCategory10);

//Create a pie D3 object, the value is [1] of the data, [0] is the name of the shop  
const pie = d3.pie()
  .value(function(d) {return d[1]})
const data_ready = pie(Object.entries(data))

//Using the precalculated radius to generate an arc D3 Object to be used for the slices
const arcGenerator = d3.arc()
  .innerRadius(0)
  .outerRadius(radius)

//Creating slices (SVG Paths) using the arc generator, 
pie_svg
  .selectAll('mySlices')
  .data(data_ready)
  .join('path')
    .attr('d', arcGenerator)
    .attr('fill', function(d){ return(color(d.index)) })
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)

//Adding a label to each slice, with the name of the shop and percent of total diamonds transcated
//The transforn angle is based on the median angle of the slice, between 0 and 90 degrees, the text is rotated 90
//Over 90, rotated 180 degrees and NaN will be 0
//This produces an effect of not needing to tilt your head to read
//While making sure the text fits in the slice 
pie_svg
  .selectAll('mySlices')
  .data(data_ready)
  .join('text')
  .text(function(d){ return d.data[0] + ` - ${Math.round((d.data[1] / 6202)*100)}%`})
  .attr('transform', function(d) {
    d.angle = (d.endAngle + d.startAngle) / 2
    if (d.angle == NaN) { return "rotate(270)" }
    var finalRot = ""
    if ((d.angle * 180 / Math.PI - 90) < 0) { finalRot = "rotate(15)" } else if ((d.angle * 180 / Math.PI - 90) > 90) { finalRot = "rotate(180)" } else { finalRot = "rotate(0)" }
    return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")" +
        "translate(" + (190) + ")" +
        finalRot
})  .style("text-anchor", "middle")
  .style("font-size", 15)