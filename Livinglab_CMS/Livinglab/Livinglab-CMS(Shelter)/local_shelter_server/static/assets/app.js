var jScript = document.createElement("script");
jScript.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js";
document.body.appendChild(jScript);

const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");
const colors = document.getElementsByClassName("jsColor");
const range = document.getElementById("jsRange");
const mode = document.getElementById("jsMode");
const saveBtn = document.getElementById("jsSave");

const INITIAL_COLOR = "#000000";
const CANVAS_SIZE = 1000;

ctx.strokeStyle = "#2c2c2c";

canvas.width = CANVAS_SIZE;
canvas.height = CANVAS_SIZE;

ctx.fillStyle = "white";
ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

ctx.strokeStyle = INITIAL_COLOR;
ctx.fillStyle = INITIAL_COLOR;
ctx.lineWidth = 2.5; /* 라인 굵기 */

let painting = false;
let filling = false;

function stopPainting() {
    painting = false;
}

function startPainting() {
    painting = true;
}

function onMouseMove(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    if (!painting) {
        ctx.beginPath();
        ctx.moveTo(x, y);
    } else{
        ctx.lineTo(x, y);
        ctx.stroke();
    }
}

function handleColorClick(event) {
  const color = event.target.style.backgroundColor;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
}

function handleRangeChange(event) {
    const size = event.target.value;
    ctx.lineWidth = size;
  }

function handleModeClick() {
 if (filling === true) {
   filling = false;
   mode.innerText = "Fill";
 } else {
  filling = true;
  mode.innerText = "Paint";
 }
}

function handleCanvasClick() {
    if (filling) {
      ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    }
  }

// 우클릭 방지
/*
function handleCM(event) {
   event.preventDefault();
 }
 */

function handleSaveClick() {
    // const link = document.createElement("a");
    // link.href = image;
    // link.download = "PaintJS";
    // link.click();
    // location.reload();
    // location.replace(location.href);
    // location.href = location.href;

    //console.log(image);

     var dataURL = canvas.toDataURL("image/png");
     var data = dataURL.replace('data:image/png;base64,', "");
    // var data = base64DecToArr(dataURL);
     console.log(data);
     $.ajax({
         type: "POST",
         url: "paintlist",
         data: JSON.stringify({
         imgBase64: data
       })
     }).done(function(data) {
     console.log(data);
     });
    location.reload();
    location.replace(location.href);
    location.href = location.href;

  //   let imageBlob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
  //
  // let formData = new FormData();
  // formData.append("image", imageBlob, "image.png");
  //
  // // modify the url accordingly
  // let response = await fetch('http://localhost:8000/image', {
  //   method: 'POST',
  //   body: formData
  // });
  //
  // // convert the response to json, modify it accordingly based on the returned response from your remote server
  // let result = await response.json();
  //
  // location.reload();
  //   location.replace(location.href);
  //   location.href = location.href;
}

Array.from(colors).forEach(color =>
    color.addEventListener("click", handleColorClick));


if (range) {
    range.addEventListener("input", handleRangeChange);
}

if (mode) {
    mode.addEventListener("click", handleModeClick);
}

if (saveBtn){
  saveBtn.addEventListener("click", handleSaveClick);
}


// touch

const state = {
  mousedown: false
};

// =====================
// == Event Listeners ==
// =====================
canvas.addEventListener('mousedown', handleWritingStart);
canvas.addEventListener('mousemove', handleWritingInProgress);
canvas.addEventListener('mouseup', handleDrawingEnd);
canvas.addEventListener('mouseout', handleDrawingEnd);

canvas.addEventListener('touchstart', handleWritingStart);
canvas.addEventListener('touchmove', handleWritingInProgress);
canvas.addEventListener('touchend', handleDrawingEnd);

canvas.addEventListener("mousemove", onMouseMove);
canvas.addEventListener("mousedown", startPainting);
canvas.addEventListener("mouseup", stopPainting);
canvas.addEventListener("mouseleave", stopPainting);
canvas.addEventListener("click", handleCanvasClick);

// ====================
// == Event Handlers ==
// ====================
function handleWritingStart(event) {
  event.preventDefault();

  const mousePos = getMosuePositionOnCanvas(event);

  ctx.beginPath();

  ctx.moveTo(mousePos.x, mousePos.y);
  const size = event.target.value;
  ctx.lineWidth = size;
  const color = event.target.style.backgroundColor;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;

  state.mousedown = true;
}

function handleWritingInProgress(event) {
  event.preventDefault();

  if (state.mousedown) {
    const mousePos = getMosuePositionOnCanvas(event);

    ctx.lineTo(mousePos.x, mousePos.y);
    ctx.stroke();
  }
}

function handleDrawingEnd(event) {
  event.preventDefault();

  if (state.mousedown) {
    ctx.shadowColor = '#333';

    ctx.stroke();
  }

  state.mousedown = false;
}

// ======================
// == Helper Functions ==
// ======================
function getMosuePositionOnCanvas(event) {
  const clientX = event.clientX || event.touches[0].clientX;
  const clientY = event.clientY || event.touches[0].clientY;
  const { offsetLeft, offsetTop } = event.target;
  const canvasX = clientX - offsetLeft;
  const canvasY = clientY - offsetTop;

  return { x: canvasX, y: canvasY };
}