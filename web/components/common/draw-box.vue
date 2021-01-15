<template>
    <div class="draw-box" ref="drawBox"></div>
</template>
<script>
import RobotDrawer from '../../utils/robot/robot-drawer'
import '../../utils/robot/robot-drawer.css'
import '../../utils/robot/robot-drawer-theme-cocode.css'
export default {
    name: 'draw-box',
    data() {
        return {
            box: null,
            robotDrawer: null,
        }
    },
    methods: {
        initDrawing() {
            const drawBox = this.$refs.drawBox
            drawBox.innerHTML = ''
            const box = document.createElement('div');
            box.style.width = '100%';
            box.style.height = '100%';
            box.style.backgroundColor = '#ffffff';
            drawBox.appendChild(box);
            return box
        },
        initRobot() {
            const box = this.initDrawing()
            this.robotDrawer = new RobotDrawer(box)
        },
        addRobotTask(task) {
            this.robotDrawer.onTask(task)
        },
    }
}
</script>
<style scoped>
    .draw-box {
        width: 100%;
        height: 100%;
    }
</style>