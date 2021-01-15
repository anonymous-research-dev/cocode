import RobotDrawer from './robot-drawer';
import './robot-drawer.css';
import './robot-drawer-theme-cocode.css';

window.cocode = window.cocode || {};
const cocode = window.cocode;

window.addEventListener('cocode-runner-robot-init', () => {
    const box = document.createElement('div');
    box.style.width = '100%';
    box.style.height = `${cocode.outputBox.offsetWidth}px`;
    box.style.backgroundColor = '#ffffff';
    cocode.outputBox.appendChild(box);
    cocode.robotDrawer = new RobotDrawer(box);
});

window.addEventListener('cocode-runner-robot-draw', e => {
    const msg = e.detail;
    cocode.robotDrawer.onTask(msg);
});