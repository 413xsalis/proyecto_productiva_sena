import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ExcelService } from '../../services/excel.service';

@Component({
  selector: 'app-excel-upload',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './excel-upload.component.html',
  styleUrls: ['./excel-upload.component.css']
})
export class ExcelUploadComponent implements OnInit {
  uploadForm!: FormGroup;
  selectedFile: File | null = null;
  isDragging = false;
  isLoading = false;
  isDeleting = false;
  isProcessing = false;
  processingFileId: number | null = null;
  processingProgress = 0;
  message = '';
  messageType: 'success' | 'error' = 'success';
  userFiles: any[] = [];
  
  // Propiedades del dashboard
  userName: string = 'admin12';
  userEmail: string = 'admin@example.com';

  constructor(
    private fb: FormBuilder,
    private excelService: ExcelService,
    private router: Router
  ) {}

  ngOnInit() {
    this.uploadForm = this.fb.group({
      file: [null]
    });
    this.loadMyFiles();
  }

  // Métodos del dashboard
  getUserInitials(): string {
    return this.userName
      .split(' ')
      .map(name => name[0])
      .join('')
      .toUpperCase();
  }

  navigateToDashboard() {
    this.router.navigate(['/dashboard']);
  }

  // Resto de métodos existentes...
  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.handleFile(file);
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  handleFile(file: File) {
    const allowedExtensions = ['.xls', '.xlsx'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!fileExtension || !allowedExtensions.includes(fileExtension)) {
      this.showMessage('Solo se permiten archivos Excel (.xls, .xlsx)', 'error');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      this.showMessage('El archivo no debe superar los 10MB', 'error');
      return;
    }

    this.selectedFile = file;
    this.showMessage(`Archivo seleccionado: ${file.name}`, 'success');
  }

  removeFile() {
    this.selectedFile = null;
    this.uploadForm.reset();
  }

  onSubmit() {
    if (!this.selectedFile) {
      this.showMessage('Por favor selecciona un archivo', 'error');
      return;
    }

    this.isLoading = true;
    this.excelService.uploadExcelFile(this.selectedFile).subscribe({
      next: (response: any) => {
        this.isLoading = false;
        this.showMessage('✅ Archivo subido exitosamente', 'success');
        this.selectedFile = null;
        this.uploadForm.reset();
        this.loadMyFiles();
      },
      error: (error: any) => {
        this.isLoading = false;
        console.error('Error al subir archivo:', error);
        this.showMessage(error.error?.detail || '❌ Error al subir archivo', 'error');
      }
    });
  }

  processFile(fileId: number) {
    this.isProcessing = true;
    this.processingFileId = fileId;
    this.processingProgress = 0;

    // Simular progreso
    const progressInterval = setInterval(() => {
      this.processingProgress += 10;
      if (this.processingProgress >= 90) {
        clearInterval(progressInterval);
      }
    }, 300);

    this.excelService.processExcelFile(fileId).subscribe({
      next: (response: any) => {
        clearInterval(progressInterval);
        this.processingProgress = 100;
        
        setTimeout(() => {
          this.isProcessing = false;
          this.processingFileId = null;
          this.processingProgress = 0;
          this.showMessage(`✅ Archivo procesado: ${response.total_rows} filas procesadas`, 'success');
          this.loadMyFiles();
        }, 500);
      },
      error: (error: any) => {
        clearInterval(progressInterval);
        this.isProcessing = false;
        this.processingFileId = null;
        this.processingProgress = 0;
        console.error('Error al procesar archivo:', error);
        this.showMessage(error.error?.detail || '❌ Error al procesar archivo', 'error');
      }
    });
  }

  loadMyFiles() {
    this.excelService.getMyFiles().subscribe({
      next: (files: any) => {
        this.userFiles = files;
      },
      error: (error: any) => {
        console.error('Error al cargar archivos:', error);
        this.showMessage('❌ Error al cargar la lista de archivos', 'error');
      }
    });
  }

  deleteFile(fileId: number, fileName: string) {
    if (!confirm(`¿Estás seguro de que quieres eliminar el archivo "${fileName}"? Esta acción no se puede deshacer.`)) {
      return;
    }

    this.isDeleting = true;
    this.excelService.deleteExcelFile(fileId).subscribe({
      next: (response: any) => {
        this.isDeleting = false;
        this.showMessage(`✅ Archivo "${fileName}" eliminado exitosamente`, 'success');
        this.loadMyFiles();
      },
      error: (error: any) => {
        this.isDeleting = false;
        console.error('Error al eliminar archivo:', error);
        this.showMessage(error.error?.detail || '❌ Error al eliminar archivo', 'error');
      }
    });
  }

  downloadFile(fileId: number, fileName: string) {
    this.showMessage('📥 Función de descarga en desarrollo...', 'success');
  }

  private showMessage(message: string, type: 'success' | 'error') {
    this.message = message;
    this.messageType = type;
    setTimeout(() => {
      this.message = '';
    }, 5000);
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  getDataKeys(data: any): string[] {
    if (!data || data.length === 0) return [];
    return Object.keys(data[0]);
  }
}