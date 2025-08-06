const modeloER = {
      USUARIO: [
        { campo: 'id', tipo: 'number' },
        { campo: 'email', tipo: 'email' },
        { campo: 'password_hash', tipo: 'text' },
        { campo: 'rol', tipo: 'text' },
        { campo: 'fecha_creacion', tipo: 'datetime-local' }
      ],
      ESTUDIANTE: [
        { campo: 'id', tipo: 'number' },
        { campo: 'usuario_id', tipo: 'number' },
        { campo: 'matricula', tipo: 'text' },
        { campo: 'carrera', tipo: 'text' }
      ],
      DOCENTE: [
        { campo: 'id', tipo: 'number' },
        { campo: 'usuario_id', tipo: 'number' },
        { campo: 'departamento', tipo: 'text' },
        { campo: 'especialidad', tipo: 'text' }
      ],
      ADMINISTRATIVO: [
        { campo: 'id', tipo: 'number' },
        { campo: 'usuario_id', tipo: 'number' },
        { campo: 'puesto', tipo: 'text' }
      ],
      PAGO: [
        { campo: 'id', tipo: 'number' },
        { campo: 'estudiante_id', tipo: 'number' },
        { campo: 'monto', tipo: 'number', step: '0.01' },
        { campo: 'concepto', tipo: 'text' },
        { campo: 'estado', tipo: 'text' }
      ],
      INSCRIPCION: [
        { campo: 'id', tipo: 'number' },
        { campo: 'estudiante_id', tipo: 'number' },
        { campo: 'clase_id', tipo: 'number' },
        { campo: 'fecha_inscripcion', tipo: 'datetime-local' }
      ],
      CALIFICACION: [
        { campo: 'id', tipo: 'number' },
        { campo: 'estudiante_id', tipo: 'number' },
        { campo: 'clase_id', tipo: 'number' },
        { campo: 'nota', tipo: 'number', step: '0.1' },
        { campo: 'tipo_evaluacion', tipo: 'text' }
      ],
      MATERIA: [
        { campo: 'id', tipo: 'number' },
        { campo: 'nombre', tipo: 'text' },
        { campo: 'codigo', tipo: 'text' }
      ],
      CLASE: [
        { campo: 'id', tipo: 'number' },
        { campo: 'materia_id', tipo: 'number' },
        { campo: 'docente_id', tipo: 'number' },
        { campo: 'horario', tipo: 'text' },
        { campo: 'aula', tipo: 'text' }
      ]
    };

    const selectEntidad = document.getElementById('tabla');
    const formulario = document.getElementById('formularioEntidad');

    // Cargar entidades al dropdown
    for (let entidad in modeloER) {
      const option = document.createElement('option');
      option.value = entidad;
      option.textContent = entidad;
      selectEntidad.appendChild(option);
    }

    // Mostrar campos dinámicos al seleccionar entidad
    selectEntidad.addEventListener('change', function () {
      formulario.innerHTML = '';
      const seleccion = this.value;
      if (!seleccion) return;

      modeloER[seleccion].forEach(campo => {
        const label = document.createElement('label');
        label.textContent = campo.campo;

        const input = document.createElement('input');
        input.name = campo.campo;
        input.type = campo.tipo || 'text';
        if (campo.step) input.step = campo.step;

        formulario.appendChild(label);
        formulario.appendChild(input);
      });

      const boton = document.createElement('button');
      boton.type = 'submit';
      boton.textContent = 'Guardar ' + seleccion;
      formulario.appendChild(boton);
    });

    // Mostrar datos en consola (simulación de guardado)
    formulario.addEventListener('submit', function (e) {
      e.preventDefault();
      const datos = {};
      [...formulario.elements].forEach(input => {
        if (input.name) datos[input.name] = input.value;
      });
      console.log("📦 Datos enviados:", datos);
      alert("✅ Datos registrados en consola.");
      formulario.reset();
    });