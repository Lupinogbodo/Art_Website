const canvas = document.getElementById('bg');
const ctx = canvas.getContext('2d');
let W, H, tris = [];

function resize() {
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

class Tri {
  constructor() {
    // center
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    // max radius of shape
    this.size = 30 + Math.random() * 70;
    // vertical speed
    this.speed = 0.2 + Math.random() * 0.5;
    // sideways drift
    this.drift = Math.random() * 1 - 0.5;
    // random offsets for 3 vertices
    this.offsets = Array.from({ length: 3 }, () => {
      const angle = Math.random() * 2 * Math.PI;
      const r = Math.random() * this.size;
      return { dx: Math.cos(angle) * r, dy: Math.sin(angle) * r };
    });
  }
  update() {
    this.y -= this.speed;
    this.x += this.drift;
    // wrap around top/bottom
    if (this.y + this.size < 0) this.y = H + this.size;
    if (this.x - this.size > W) this.x = -this.size;
    if (this.x + this.size < 0) this.x = W + this.size;
  }
  draw() {
    ctx.beginPath();
    const v0 = this.offsets[0],
          v1 = this.offsets[1],
          v2 = this.offsets[2];
    ctx.moveTo(this.x + v0.dx, this.y + v0.dy);
    ctx.lineTo(this.x + v1.dx, this.y + v1.dy);
    ctx.lineTo(this.x + v2.dx, this.y + v2.dy);
    ctx.closePath();
    ctx.strokeStyle = '#111';
    ctx.stroke();
  }
}

// initialize
for (let i = 0; i < 40; i++) {
  tris.push(new Tri());
}

function animate() {
  ctx.clearRect(0, 0, W, H);
  tris.forEach(t => {
    t.update();
    t.draw();
  });
  requestAnimationFrame(animate);
}
animate();
