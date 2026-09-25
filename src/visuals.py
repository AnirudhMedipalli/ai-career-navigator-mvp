import streamlit as st


CAREER_SCENE = st.components.v2.component(
    "career_navigator_growth_scene",
    html='<canvas class="growth-scene" role="img" aria-label="A 3D path of rising skill milestones"></canvas>',
    css="""
    .growth-scene { display: block; width: 100%; height: 100%; outline: none; }
    """,
    js="""
    export default function ({ parentElement }) {
      const canvas = parentElement.querySelector("canvas")
      let renderer
      let frameId
      let disposed = false
      let pointerX = 0
      let pointerY = 0
      let resizeObserver

      const onPointerMove = (event) => {
        const bounds = canvas.getBoundingClientRect()
        pointerX = ((event.clientX - bounds.left) / bounds.width - 0.5) * 2
        pointerY = ((event.clientY - bounds.top) / bounds.height - 0.5) * 2
      }

      import("https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js")
        .then((THREE) => {
          if (disposed) return

          const scene = new THREE.Scene()
          const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 60)
          camera.position.set(0, 0.2, 10.5)
          renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true })
          renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.7))
          renderer.setClearColor(0x000000, 0)

          scene.add(new THREE.HemisphereLight(0xe8e4ff, 0x18233a, 2.1))
          const keyLight = new THREE.DirectionalLight(0xffffff, 2.7)
          keyLight.position.set(-3, 5, 7)
          scene.add(keyLight)

          const path = new THREE.Group()
          scene.add(path)
          const stepColors = [0x6c5ce7, 0x786bed, 0x8a7df2, 0x8be0c2, 0x8be0c2, 0xf2ad75]
          const points = []

          for (let index = 0; index < 6; index += 1) {
            const x = -3.05 + index * 1.12
            const y = -1.52 + index * 0.49
            const height = 0.28 + index * 0.025
            const material = new THREE.MeshStandardMaterial({
              color: stepColors[index],
              roughness: 0.34,
              metalness: 0.22,
              emissive: stepColors[index],
              emissiveIntensity: index > 2 ? 0.13 : 0.05,
            })
            const block = new THREE.Mesh(
              new THREE.BoxGeometry(0.88, height, 0.82),
              material,
            )
            block.position.set(x, y + height / 2, 0)
            path.add(block)
            points.push(new THREE.Vector3(x, y + height + 0.05, 0.44))

            const edge = new THREE.LineSegments(
              new THREE.EdgesGeometry(block.geometry),
              new THREE.LineBasicMaterial({ color: 0xd5d9ff, transparent: true, opacity: 0.23 }),
            )
            edge.position.copy(block.position)
            path.add(edge)
          }

          const trajectory = new THREE.CatmullRomCurve3(points)
          path.add(new THREE.Mesh(
            new THREE.TubeGeometry(trajectory, 80, 0.025, 8, false),
            new THREE.MeshBasicMaterial({ color: 0xb4ffe7, transparent: true, opacity: 0.82 }),
          ))

          const beacon = new THREE.Group()
          beacon.position.copy(points[points.length - 1])
          beacon.position.y += 0.72
          path.add(beacon)
          const crystal = new THREE.Mesh(
            new THREE.OctahedronGeometry(0.48, 0),
            new THREE.MeshStandardMaterial({
              color: 0xffc18b,
              roughness: 0.2,
              metalness: 0.58,
              emissive: 0xa84b6d,
              emissiveIntensity: 0.36,
            }),
          )
          beacon.add(crystal)
          beacon.add(new THREE.LineSegments(
            new THREE.EdgesGeometry(crystal.geometry),
            new THREE.LineBasicMaterial({ color: 0xffe3c7, transparent: true, opacity: 0.78 }),
          ))

          const grid = new THREE.GridHelper(13, 26, 0x74809a, 0x344158)
          grid.position.set(0, -1.78, -0.68)
          grid.material.transparent = true
          grid.material.opacity = 0.22
          scene.add(grid)

          const resize = () => {
            const bounds = canvas.getBoundingClientRect()
            const width = Math.max(1, bounds.width)
            const height = Math.max(1, bounds.height)
            renderer.setSize(width, height, false)
            camera.aspect = width / height
            camera.position.z = width < 420 ? 12.4 : width < 650 ? 11.3 : 10.5
            camera.updateProjectionMatrix()
          }
          resizeObserver = new ResizeObserver(resize)
          resizeObserver.observe(canvas)
          resize()
          canvas.addEventListener("pointermove", onPointerMove)

          const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
          const animate = (time) => {
            if (disposed) return
            path.rotation.y += (pointerX * 0.12 - path.rotation.y) * 0.025
            path.rotation.x += (-pointerY * 0.045 - path.rotation.x) * 0.025
            beacon.rotation.y = reduceMotion ? 0 : time * 0.00035
            crystal.rotation.x = reduceMotion ? 0 : Math.sin(time * 0.00045) * 0.12
            renderer.render(scene, camera)
            if (!reduceMotion) frameId = requestAnimationFrame(animate)
          }
          animate(0)
        })
        .catch(() => {
          if (!disposed) canvas.setAttribute("aria-label", "3D career path preview could not load")
        })

      return () => {
        disposed = true
        cancelAnimationFrame(frameId)
        resizeObserver?.disconnect()
        canvas.removeEventListener("pointermove", onPointerMove)
        renderer?.dispose()
      }
    }
    """,
)