/**
 * Module 10: Drag-and-Drop File Upload with Image Preview
 * Features:
 * - HTML5 Drag & Drop zone with visual feedback
 * - File picker click fallback
 * - Client-side MIME type and size validation (max 5MB)
 * - Instant live thumbnail preview using URL.createObjectURL
 * - File remove / reset button
 */

const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024; // 5 MB
const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];

export function handleFileSelection(file, dropZone, input) {
  const errorEl = dropZone.querySelector('.upload-error') || dropZone.nextElementSibling;
  const previewContainer = dropZone.querySelector('.upload-preview');

  const setError = (msg) => {
    if (errorEl) {
      errorEl.textContent = msg;
      errorEl.style.display = 'block';
    }
    dropZone.classList.add('has-error');
  };

  const clearError = () => {
    if (errorEl) {
      errorEl.textContent = '';
      errorEl.style.display = 'none';
    }
    dropZone.classList.remove('has-error');
  };

  clearError();

  if (!file) {
    return;
  }

  // Size validation
  if (file.size > MAX_FILE_SIZE_BYTES) {
    setError(`File too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Maximum allowed size is 5 MB.`);
    input.value = '';
    return;
  }

  // MIME type validation
  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    setError(`Invalid file type "${file.type}". Please upload a JPEG, PNG, or WebP image.`);
    input.value = '';
    return;
  }

  // Generate preview
  if (previewContainer) {
    const objectUrl = URL.createObjectURL(file);
    previewContainer.innerHTML = `
      <div class="preview-card d-flex items-center gap-md p-md border rounded mt-md">
        <img src="${objectUrl}" alt="Preview" class="preview-thumbnail" style="width: 64px; height: 64px; object-fit: cover; border-radius: 8px;">
        <div class="flex-1">
          <strong class="d-block text-truncate" style="max-width: 200px;">${file.name}</strong>
          <small class="text-muted">${(file.size / 1024).toFixed(0)} KB</small>
        </div>
        <button type="button" class="btn btn--secondary btn--sm btn-remove-preview" aria-label="Remove image">&times;</button>
      </div>
    `;
    previewContainer.style.display = 'block';

    const removeBtn = previewContainer.querySelector('.btn-remove-preview');
    if (removeBtn) {
      removeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        input.value = '';
        URL.revokeObjectURL(objectUrl);
        previewContainer.innerHTML = '';
        previewContainer.style.display = 'none';
        clearError();
      });
    }
  }
}

export function initFileUpload() {
  const dropZones = document.querySelectorAll('[data-drop-zone], .upload-dropzone');
  dropZones.forEach((zone) => {
    const input = zone.querySelector('input[type="file"]') || document.getElementById(zone.dataset.for);
    if (!input) {
      return;
    }

    zone.addEventListener('click', (e) => {
      if (!e.target.closest('.btn-remove-preview')) {
        input.click();
      }
    });

    ['dragenter', 'dragover'].forEach((eventName) => {
      zone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        zone.classList.add('is-dragover');
      });
    });

    ['dragleave', 'dragend', 'drop'].forEach((eventName) => {
      zone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        zone.classList.remove('is-dragover');
      });
    });

    zone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        input.files = files;
        handleFileSelection(files[0], zone, input);
      }
    });

    input.addEventListener('change', () => {
      if (input.files && input.files.length > 0) {
        handleFileSelection(input.files[0], zone, input);
      }
    });
  });
}
