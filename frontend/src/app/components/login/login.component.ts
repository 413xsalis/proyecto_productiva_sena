import { Component, OnInit } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'] // ✅ COMA AGREGADA después de templateUrl
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  registerForm!: FormGroup;
  message = '';
  isLoading = false;
  backendStatus = 'checking';
  isLoginMode = true;

  constructor(
    private fb: FormBuilder, 
    private auth: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loginForm = this.fb.group({
      username: ['admin', Validators.required],
      password: ['1234', Validators.required],
    });

    this.registerForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(4)]],
      confirmPassword: ['', Validators.required]
    });

    this.checkBackendHealth();
  }

  switchMode() {
    this.isLoginMode = !this.isLoginMode;
    this.message = '';
    this.loginForm.reset();
    this.registerForm.reset();
    
    if (this.isLoginMode) {
      this.loginForm.patchValue({
        username: 'admin',
        password: '1234'
      });
    }
  }

  checkBackendHealth(): void {
    this.auth.checkHealth().subscribe({
      next: (response: any) => {
        this.backendStatus = 'online';
        console.log('✅ Backend conectado:', response);
      },
      error: (error: any) => {
        this.backendStatus = 'offline';
        console.error('❌ Backend no disponible:', error);
        this.message = 'El servidor no está disponible';
      }
    });
  }

  onLogin(): void {
    if (this.loginForm.invalid || this.isLoading) {
      return;
    }

    this.isLoading = true;
    this.message = '';

    const username = this.loginForm.get('username')?.value;
    const password = this.loginForm.get('password')?.value;

    console.log('🔄 Intentando login con:', { username, password });

    this.auth.login(username, password).subscribe({
      next: (res: any) => {
        console.log('✅ Login exitoso', res);
        this.isLoading = false;
        this.message = 'Inicio de sesión exitoso 🎉';
        
        setTimeout(() => {
          this.router.navigate(['/dashboard']);
        }, 1000);
      },
      error: (err: any) => {
        console.error('❌ Error en login:', err);
        this.isLoading = false;
        
        if (err.status === 0) {
          this.message = 'Error de conexión con el servidor';
        } else if (err.status === 401) {
          this.message = 'Usuario o contraseña incorrectos';
        } else if (err.status === 400) {
          this.message = 'Datos inválidos';
        } else {
          this.message = err.error?.detail || 'Error en inicio de sesión';
        }
      }
    });
  }

  onRegister(): void {
    if (this.registerForm.invalid || this.isLoading) {
      return;
    }

    const password = this.registerForm.get('password')?.value;
    const confirmPassword = this.registerForm.get('confirmPassword')?.value;
    
    if (password !== confirmPassword) {
      this.message = 'Las contraseñas no coinciden';
      return;
    }

    this.isLoading = true;
    this.message = '';

    const userData = {
      username: this.registerForm.get('username')?.value,
      email: this.registerForm.get('email')?.value,
      password: password
    };

    console.log('🔄 Intentando registro con:', userData);

    this.auth.register(userData).subscribe({
      next: (res: any) => {
        console.log('✅ Registro exitoso', res);
        this.isLoading = false;
        this.message = '¡Registro exitoso! 🎉 Ahora puedes iniciar sesión';
        
        setTimeout(() => {
          this.isLoginMode = true;
          this.message = 'Por favor inicia sesión con tu nueva cuenta';
        }, 2000);
      },
      error: (err: any) => {
        console.error('❌ Error en registro:', err);
        this.isLoading = false;
        
        if (err.status === 0) {
          this.message = 'Error de conexión con el servidor';
        } else if (err.status === 400) {
          this.message = err.error?.detail || 'Error en el registro - Verifica los datos';
        } else {
          this.message = err.error?.detail || 'Error en el registro';
        }
      }
    });
  }

  get token(): string | null {
    return this.auth.getToken();
  }

  get lf() { return this.loginForm.controls; }
  get rf() { return this.registerForm.controls; }
}