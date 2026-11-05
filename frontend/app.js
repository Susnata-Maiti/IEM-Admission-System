/**
 * Frontend Single Page Application Logic for IEM Admission System
 * Implements FR-01 through FR-20, NFR-01 to NFR-05, and Wireframes.
 */

const API_BASE = "";
let currentUser = null;
let currentToken = null;
let currentApplication = null;
let activeStep = 1;
let selectedFile = null;
let currentViewMode = "table"; // 'table' or 'card'
let cachedApplications = [];
let activeModalAppId = null;

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  initSession();
  loadCourses();
});

// Toast Notifications (FR-07)
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  
  const icon = type === "success" ? "fa-circle-check" : type === "error" ? "fa-circle-exclamation" : "fa-circle-info";
  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// --------------------------------------------------------------------------
// Session & Auth Handling
// --------------------------------------------------------------------------

function initSession() {
  const token = localStorage.getItem("iem_token");
  const user = localStorage.getItem("iem_user");

  if (token && user) {
    currentToken = token;
    currentUser = JSON.parse(user);
    renderNav();
    routeUser();
  } else {
    renderNav();
    showView("authSection");
  }
}

function renderNav() {
  const navSection = document.getElementById("navAuthSection");
  if (currentUser) {
    const roleClass = `role-${currentUser.role}`;
    navSection.innerHTML = `
      <div class="nav-user-pill">
        <i class="fa-solid fa-circle-user"></i>
        <span>${escapeHtml(currentUser.name)}</span>
        <span class="nav-role-badge ${roleClass}">${currentUser.role}</span>
        <button class="btn btn-sm btn-outline" onclick="handleLogout()" title="Log Out">
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
        </button>
      </div>
    `;
  } else {
    navSection.innerHTML = `
      <span style="font-size: 0.84rem; color: #64748b; font-weight: 600;">
        <i class="fa-solid fa-shield-halved"></i> Secure Portal
      </span>
    `;
  }
}

function routeUser() {
  if (!currentUser) {
    showView("authSection");
    return;
  }
  if (currentUser.role === "student") {
    showView("studentSection");
    loadStudentDashboard();
  } else if (currentUser.role === "admin" || currentUser.role === "director") {
    showView("adminSection");
    loadAdminDashboard();
  }
}

function showView(viewId) {
  document.querySelectorAll(".view-section").forEach(sec => {
    sec.classList.remove("active");
    sec.classList.add("hidden");
  });
  const target = document.getElementById(viewId);
  if (target) {
    target.classList.remove("hidden");
    target.classList.add("active");
  }
}

function switchAuthTab(tab) {
  const tabLogin = document.getElementById("tabLogin");
  const tabRegister = document.getElementById("tabRegister");
  const formLogin = document.getElementById("loginForm");
  const formRegister = document.getElementById("registerForm");

  if (tab === "login") {
    tabLogin.classList.add("active");
    tabRegister.classList.remove("active");
    formLogin.classList.remove("hidden");
    formRegister.classList.add("hidden");
  } else {
    tabRegister.classList.add("active");
    tabLogin.classList.remove("active");
    formRegister.classList.remove("hidden");
    formLogin.classList.add("hidden");
  }
}

function prefillLogin(email, password) {
  switchAuthTab("login");
  document.getElementById("loginEmail").value = email;
  document.getElementById("loginPassword").value = password;
}

// FR-01: Password Requirements Dynamic Checker
function checkPasswordRequirements(pwd) {
  const ruleLen = document.getElementById("ruleLength");
  const ruleUpper = document.getElementById("ruleUpper");
  const ruleSpecial = document.getElementById("ruleSpecial");

  const isLen = pwd.length >= 8;
  const isUpper = /[A-Z]/.test(pwd);
  const isSpecial = /[!@#$%^&*(),.?":{}|<>\-_=+/~`]/.test(pwd);

  toggleRule(ruleLen, isLen);
  toggleRule(ruleUpper, isUpper);
  toggleRule(ruleSpecial, isSpecial);
}

function toggleRule(el, valid) {
  if (valid) {
    el.classList.add("valid");
    el.querySelector("i").className = "fa-solid fa-circle-check";
  } else {
    el.classList.remove("valid");
    el.querySelector("i").className = "fa-solid fa-circle-xmark";
  }
}

async function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value;

  try {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Login failed");

    localStorage.setItem("iem_token", data.token);
    localStorage.setItem("iem_user", JSON.stringify(data.user));
    currentToken = data.token;
    currentUser = data.user;

    showToast(`Welcome back, ${currentUser.name}!`, "success");
    renderNav();
    routeUser();
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const name = document.getElementById("regName").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value;

  try {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Registration failed");

    localStorage.setItem("iem_token", data.token);
    localStorage.setItem("iem_user", JSON.stringify(data.user));
    currentToken = data.token;
    currentUser = data.user;

    showToast("Registration successful! Complete your application below.", "success");
    renderNav();
    routeUser();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function handleLogout() {
  localStorage.removeItem("iem_token");
  localStorage.removeItem("iem_user");
  currentToken = null;
  currentUser = null;
  showToast("Logged out successfully.", "info");
  renderNav();
  showView("authSection");
}

// --------------------------------------------------------------------------
// Courses Loading (FR-04, NFR-03)
// --------------------------------------------------------------------------

async function loadCourses() {
  try {
    const res = await fetch(`${API_BASE}/api/courses`);
    const data = await res.json();
    
    // Populate Wizard dropdown
    const wizardSelect = document.getElementById("appCourse");
    if (wizardSelect) {
      wizardSelect.innerHTML = '<option value="">-- Select Programme Choice --</option>';
      data.courses.forEach(c => {
        wizardSelect.innerHTML += `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`;
      });
    }

    // Populate Filter dropdown
    const filterSelect = document.getElementById("filterCourseSelect");
    if (filterSelect) {
      filterSelect.innerHTML = '<option value="">All Courses</option>';
      data.courses.forEach(c => {
        filterSelect.innerHTML += `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`;
      });
    }
  } catch (err) {
    console.error("Failed to load courses:", err);
  }
}

// --------------------------------------------------------------------------
// Student Portal & Application Wizard (FR-03 to FR-11)
// --------------------------------------------------------------------------

async function loadStudentDashboard() {
  document.getElementById("studentWelcomeName").textContent = currentUser.name;
  document.getElementById("studentEmailLabel").textContent = currentUser.email;

  try {
    const res = await fetch(`${API_BASE}/api/student/application`, {
      headers: { "Authorization": `Bearer ${currentToken}` }
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to load application");

    currentApplication = data.application;
    renderStudentView();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function renderStudentView() {
  const statusBadge = document.getElementById("studentStatusBadge");
  const formView = document.getElementById("studentFormView");
  const submittedView = document.getElementById("studentSubmittedView");

  const status = currentApplication.status;
  statusBadge.className = `badge badge-${status.toLowerCase().replace(/\s+/g, '-')}`;
  statusBadge.textContent = status;

  if (status === "Draft") {
    // Mode B: Interactive Wizard
    formView.classList.remove("hidden");
    submittedView.classList.add("hidden");

    // Populate existing draft data
    document.getElementById("appFullName").value = currentApplication.full_name || currentUser.name;
    document.getElementById("appDob").value = currentApplication.dob || "";
    document.getElementById("appContact").value = currentApplication.contact_number || "";
    document.getElementById("appAddress").value = currentApplication.address || "";
    document.getElementById("appClass10Marks").value = currentApplication.class_10_marks || "";
    document.getElementById("appClass10Board").value = currentApplication.class_10_board || "";
    document.getElementById("appClass12Marks").value = currentApplication.class_12_marks || "";
    document.getElementById("appClass12Board").value = currentApplication.class_12_board || "";
    if (currentApplication.passing_year) {
      document.getElementById("appPassingYear").value = currentApplication.passing_year;
    }
    if (currentApplication.course) {
      document.getElementById("appCourse").value = currentApplication.course;
    }
    if (currentApplication.doc_filename) {
      showFileStatus(currentApplication.doc_filename, "Uploaded previously");
    }
  } else {
    // Mode A: Locked Submitted View (FR-09, FR-10, FR-11)
    formView.classList.add("hidden");
    submittedView.classList.remove("hidden");

    document.getElementById("subAppCode").textContent = currentApplication.app_code;
    document.getElementById("subFullName").textContent = currentApplication.full_name;
    document.getElementById("subDob").textContent = currentApplication.dob;
    document.getElementById("subContact").textContent = currentApplication.contact_number;
    document.getElementById("subAddress").textContent = currentApplication.address;
    document.getElementById("subCourse").textContent = currentApplication.course;
    document.getElementById("subClass10").textContent = `${currentApplication.class_10_marks}% (${currentApplication.class_10_board})`;
    document.getElementById("subClass12").textContent = `${currentApplication.class_12_marks}% (${currentApplication.class_12_board})`;
    document.getElementById("subDate").textContent = currentApplication.submitted_at || "-";
    document.getElementById("subDocName").textContent = currentApplication.doc_filename || "Document.pdf";

    // Update Timeline Stepper
    updateTimelineProgress(status);

    // Remarks Notice
    const remarksNotice = document.getElementById("subRemarksNotice");
    if (currentApplication.remarks) {
      remarksNotice.classList.remove("hidden");
      document.getElementById("subRemarksText").innerHTML = `<strong>Review Remarks:</strong> ${escapeHtml(currentApplication.remarks)}`;
    } else {
      remarksNotice.classList.add("hidden");
    }
  }
}

function updateTimelineProgress(status) {
  const stepSubmit = document.getElementById("stepSubmit");
  const stepDocs = document.getElementById("stepDocs");
  const stepReview = document.getElementById("stepReview");
  const stepDecision = document.getElementById("stepDecision");
  const decisionText = document.getElementById("timelineDecisionText");

  // Reset classes
  [stepSubmit, stepDocs, stepReview, stepDecision].forEach(s => {
    s.className = "timeline-step";
  });

  stepSubmit.classList.add("completed");

  if (status === "Submitted") {
    stepDocs.classList.add("active");
    decisionText.textContent = "Awaiting verification";
  } else if (status === "Under Review") {
    stepDocs.classList.add("completed");
    stepReview.classList.add("active");
    decisionText.textContent = "Evaluation in progress";
  } else if (status === "Accepted") {
    stepDocs.classList.add("completed");
    stepReview.classList.add("completed");
    stepDecision.classList.add("completed");
    stepDecision.querySelector(".step-icon").innerHTML = '<i class="fa-solid fa-check"></i>';
    decisionText.textContent = "Congratulations! Admission Offer Issued.";
  } else if (status === "Rejected") {
    stepDocs.classList.add("completed");
    stepReview.classList.add("completed");
    stepDecision.classList.add("rejected");
    stepDecision.querySelector(".step-icon").innerHTML = '<i class="fa-solid fa-xmark"></i>';
    decisionText.textContent = "Application not selected.";
  }
}

// Wizard Step Navigation
function goToStep(step) {
  // Validate step before advancing
  if (step > activeStep) {
    if (activeStep === 1) {
      const name = document.getElementById("appFullName").value.trim();
      const dob = document.getElementById("appDob").value;
      const phone = document.getElementById("appContact").value.trim();
      const address = document.getElementById("appAddress").value.trim();
      if (!name || !dob || !phone || !address) {
        showToast("Please fill in all mandatory personal details.", "error");
        return;
      }
    } else if (activeStep === 2) {
      const c10m = document.getElementById("appClass10Marks").value;
      const c10b = document.getElementById("appClass10Board").value.trim();
      const c12m = document.getElementById("appClass12Marks").value;
      const c12b = document.getElementById("appClass12Board").value.trim();
      const course = document.getElementById("appCourse").value;
      if (!c10m || !c10b || !c12m || !c12b || !course) {
        showToast("Please complete academic scores and select a course.", "error");
        return;
      }
      if (parseFloat(c10m) < 0 || parseFloat(c10m) > 100 || parseFloat(c12m) < 0 || parseFloat(c12m) > 100) {
        showToast("Academic scores must be between 0.0% and 100.0%.", "error");
        return;
      }
    } else if (activeStep === 3) {
      if (!selectedFile && !currentApplication.doc_filename) {
        showToast("Please upload your PDF marksheet before proceeding.", "error");
        return;
      }
    }
  }

  // Update Review Screen if navigating to Step 4
  if (step === 4) {
    document.getElementById("revName").textContent = document.getElementById("appFullName").value;
    document.getElementById("revDob").textContent = document.getElementById("appDob").value;
    document.getElementById("revPhone").textContent = document.getElementById("appContact").value;
    document.getElementById("revAddress").textContent = document.getElementById("appAddress").value;
    document.getElementById("revCourse").textContent = document.getElementById("appCourse").value;
    document.getElementById("revYear").textContent = document.getElementById("appPassingYear").value;
    document.getElementById("revC10").textContent = `${document.getElementById("appClass10Marks").value}% (${document.getElementById("appClass10Board").value})`;
    document.getElementById("revC12").textContent = `${document.getElementById("appClass12Marks").value}% (${document.getElementById("appClass12Board").value})`;
    document.getElementById("revDocName").textContent = selectedFile ? selectedFile.name : (currentApplication.doc_filename || "Verified");
  }

  activeStep = step;
  for (let i = 1; i <= 4; i++) {
    const pane = document.getElementById(`wizardStep${i}`);
    const navItem = document.getElementById(`fStep${i}`);
    if (i === step) {
      pane.classList.remove("hidden");
      pane.classList.add("active");
      navItem.className = "f-step active";
    } else {
      pane.classList.remove("active");
      pane.classList.add("hidden");
      navItem.className = i < step ? "f-step done" : "f-step";
    }
  }
}

// File Selection & Drag-and-Drop (FR-05, FR-06, NFR-04)
const dropzone = document.getElementById("pdfDropzone");
if (dropzone) {
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.style.borderColor = "#1e40af";
    dropzone.style.backgroundColor = "#e0f2fe";
  });
  dropzone.addEventListener("dragleave", () => {
    dropzone.style.borderColor = "#93c5fd";
    dropzone.style.backgroundColor = "#f0f7ff";
  });
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.style.borderColor = "#93c5fd";
    dropzone.style.backgroundColor = "#f0f7ff";
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  });
}

function handleFileSelection(file) {
  if (!file) return;

  // Validate PDF format
  if (!file.name.toLowerCase().endsWith(".pdf") && file.type !== "application/pdf") {
    showToast("Invalid file type. Only PDF documents are accepted.", "error");
    return;
  }

  // Validate 5MB limit
  const maxBytes = 5 * 1024 * 1024;
  if (file.size > maxBytes) {
    showToast(`File size (${(file.size / (1024*1024)).toFixed(2)}MB) exceeds 5MB limit.`, "error");
    return;
  }

  selectedFile = file;
  const sizeStr = `${(file.size / 1024).toFixed(1)} KB`;
  showFileStatus(file.name, sizeStr);
  showToast(`PDF document '${file.name}' validated successfully.`, "success");
}

function showFileStatus(name, size) {
  const box = document.getElementById("uploadStatusBox");
  box.classList.remove("hidden");
  document.getElementById("selectedFileName").textContent = name;
  document.getElementById("selectedFileSize").textContent = size;
}

// Save & Submit Final Wizard (FR-08)
async function handleWizardSubmit(e) {
  e.preventDefault();

  const payload = {
    full_name: document.getElementById("appFullName").value.trim(),
    dob: document.getElementById("appDob").value,
    contact_number: document.getElementById("appContact").value.trim(),
    address: document.getElementById("appAddress").value.trim(),
    class_10_marks: parseFloat(document.getElementById("appClass10Marks").value),
    class_10_board: document.getElementById("appClass10Board").value.trim(),
    class_12_marks: parseFloat(document.getElementById("appClass12Marks").value),
    class_12_board: document.getElementById("appClass12Board").value.trim(),
    passing_year: parseInt(document.getElementById("appPassingYear").value),
    course: document.getElementById("appCourse").value
  };

  try {
    // 1. Save Draft Details
    const saveRes = await fetch(`${API_BASE}/api/student/application/save`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${currentToken}`
      },
      body: JSON.stringify(payload)
    });
    const saveData = await saveRes.json();
    if (!saveRes.ok) throw new Error(saveData.detail || "Failed to save draft");

    // 2. Upload Document if newly selected
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const upRes = await fetch(`${API_BASE}/api/student/application/upload`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${currentToken}` },
        body: formData
      });
      const upData = await upRes.json();
      if (!upRes.ok) throw new Error(upData.detail || "Document upload failed");
    }

    // 3. Final Submit
    const submitRes = await fetch(`${API_BASE}/api/student/application/submit`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${currentToken}` }
    });
    const submitData = await submitRes.json();
    if (!submitRes.ok) throw new Error(submitData.detail || "Submission failed");

    showToast("Application submitted successfully! Record locked.", "success");
    loadStudentDashboard();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function downloadOwnDocument() {
  if (!currentApplication) return;
  window.open(`${API_BASE}/api/documents/${currentApplication.id}?token=${currentToken}`, "_blank");
}

// --------------------------------------------------------------------------
// Administrator & Director Workspace (FR-12, FR-15, FR-16, FR-17, FR-19, FR-20)
// --------------------------------------------------------------------------

async function loadAdminDashboard() {
  await Promise.all([loadMetrics(), loadApplications()]);
}

async function loadMetrics() {
  try {
    const res = await fetch(`${API_BASE}/api/admin/metrics`, {
      headers: { "Authorization": `Bearer ${currentToken}` }
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to fetch metrics");

    const m = data.metrics;
    document.getElementById("metricTotal").textContent = m.total;
    document.getElementById("metricSubmitted").textContent = m.submitted;
    document.getElementById("metricReview").textContent = m.under_review;
    document.getElementById("metricAccepted").textContent = m.accepted;
    document.getElementById("metricRejected").textContent = m.rejected;
  } catch (err) {
    console.error("Metrics load error:", err);
  }
}

async function loadApplications() {
  const search = document.getElementById("adminSearchInput")?.value.trim() || "";
  const course = document.getElementById("filterCourseSelect")?.value || "";
  const status = document.getElementById("filterStatusSelect")?.value || "";

  let url = `${API_BASE}/api/admin/applications?`;
  if (search) url += `search=${encodeURIComponent(search)}&`;
  if (course) url += `course=${encodeURIComponent(course)}&`;
  if (status) url += `status=${encodeURIComponent(status)}&`;

  try {
    const res = await fetch(url, {
      headers: { "Authorization": `Bearer ${currentToken}` }
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to fetch applications");

    cachedApplications = data.applications;
    renderApplications();
  } catch (err) {
    showToast(err.message, "error");
  }
}

function handleSearchFilter() {
  loadApplications();
}

function setViewMode(mode) {
  currentViewMode = mode;
  const btnTable = document.getElementById("btnViewTable");
  const btnCard = document.getElementById("btnViewCard");
  const tableView = document.getElementById("adminTableView");
  const cardView = document.getElementById("adminCardView");

  if (mode === "table") {
    btnTable.classList.add("active");
    btnCard.classList.remove("active");
    tableView.classList.remove("hidden");
    cardView.classList.add("hidden");
  } else {
    btnCard.classList.add("active");
    btnTable.classList.remove("active");
    cardView.classList.remove("hidden");
    tableView.classList.add("hidden");
  }
  renderApplications();
}

function renderApplications() {
  const tbody = document.getElementById("applicationsTableBody");
  const cardsContainer = document.getElementById("adminCardView");

  if (!tbody || !cardsContainer) return;

  if (cachedApplications.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 2rem; color: #64748b;">No applications found matching your criteria.</td></tr>`;
    cardsContainer.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: #64748b;">No applications found.</div>`;
    return;
  }

  // Render Table Rows
  tbody.innerHTML = cachedApplications.map(app => {
    const statusClass = `badge-${app.status.toLowerCase().replace(/\s+/g, '-')}`;
    return `
      <tr>
        <td><strong class="code-pill">${escapeHtml(app.app_code)}</strong></td>
        <td>
          <strong>${escapeHtml(app.full_name)}</strong>
          <div style="font-size: 0.78rem; color: #64748b;">${escapeHtml(app.contact_number)}</div>
        </td>
        <td><span class="course-highlight">${escapeHtml(app.course)}</span></td>
        <td>${app.class_10_marks}% / ${app.class_12_marks}%</td>
        <td>${escapeHtml(app.submitted_at || "-")}</td>
        <td><span class="badge ${statusClass}">${escapeHtml(app.status)}</span></td>
        <td>
          <button class="btn btn-sm btn-outline" onclick="openDetailModal(${app.id})">
            <i class="fa-solid fa-eye"></i> View Details
          </button>
        </td>
      </tr>
    `;
  }).join("");

  // Render Cards (NFR-03 Detailed Card View)
  cardsContainer.innerHTML = cachedApplications.map(app => {
    const statusClass = `badge-${app.status.toLowerCase().replace(/\s+/g, '-')}`;
    return `
      <div class="app-card-item">
        <div>
          <div class="aci-header">
            <span class="code-pill">${escapeHtml(app.app_code)}</span>
            <span class="badge ${statusClass}">${escapeHtml(app.status)}</span>
          </div>
          <h4 class="aci-title">${escapeHtml(app.full_name)}</h4>
          <div class="aci-course">${escapeHtml(app.course)}</div>
          <div class="aci-details">
            <div><i class="fa-regular fa-calendar"></i> Submitted: ${escapeHtml(app.submitted_at || "-")}</div>
            <div><i class="fa-solid fa-phone"></i> Contact: ${escapeHtml(app.contact_number)}</div>
            <div><i class="fa-solid fa-chart-simple"></i> Class 10: ${app.class_10_marks}% | Class 12: ${app.class_12_marks}%</div>
          </div>
        </div>
        <button class="btn btn-sm btn-primary btn-block" onclick="openDetailModal(${app.id})">
          <i class="fa-solid fa-folder-open"></i> Open Application
        </button>
      </div>
    `;
  }).join("");
}

// Open Detail & Audit Modal (FR-13, FR-17, FR-18, FR-19)
async function openDetailModal(appId) {
  activeModalAppId = appId;
  const modal = document.getElementById("appDetailModal");

  try {
    const res = await fetch(`${API_BASE}/api/admin/applications/${appId}`, {
      headers: { "Authorization": `Bearer ${currentToken}` }
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to load application details");

    const app = data.application;
    document.getElementById("modalAppCode").textContent = app.app_code;
    document.getElementById("modalAppName").textContent = app.full_name;
    document.getElementById("mDob").textContent = app.dob;
    document.getElementById("mContact").textContent = app.contact_number;
    document.getElementById("mAddress").textContent = app.address;
    document.getElementById("mCourse").textContent = app.course;
    document.getElementById("mC10Marks").textContent = `${app.class_10_marks}%`;
    document.getElementById("mC10Board").textContent = app.class_10_board;
    document.getElementById("mC12Marks").textContent = `${app.class_12_marks}%`;
    document.getElementById("mC12Board").textContent = app.class_12_board;
    document.getElementById("mPassingYear").textContent = app.passing_year;
    document.getElementById("mDocName").textContent = app.doc_filename || "marksheet.pdf";

    // Set download link
    const dlLink = document.getElementById("mDocDownloadLink");
    dlLink.href = `${API_BASE}/api/documents/${app.id}`;
    dlLink.onclick = (e) => {
      e.preventDefault();
      fetch(`${API_BASE}/api/documents/${app.id}`, {
        headers: { "Authorization": `Bearer ${currentToken}` }
      })
      .then(r => r.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        window.open(url, "_blank");
      })
      .catch(() => showToast("Could not preview document", "error"));
    };

    // Render Audit Trail (FR-13)
    const auditContainer = document.getElementById("modalAuditTrail");
    if (app.audit_trail && app.audit_trail.length > 0) {
      auditContainer.innerHTML = app.audit_trail.map(log => `
        <div class="audit-entry">
          <div class="ae-meta">
            <span><strong>${escapeHtml(log.changed_by)}</strong></span>
            <span>${escapeHtml(log.timestamp)}</span>
          </div>
          <div class="ae-transition">${escapeHtml(log.old_status)} &rarr; ${escapeHtml(log.new_status)}</div>
          ${log.remarks ? `<div class="ae-remarks">"${escapeHtml(log.remarks)}"</div>` : ''}
        </div>
      `).join("");
    } else {
      auditContainer.innerHTML = `<div style="color: #64748b; font-size: 0.82rem;">No audit events logged yet.</div>`;
    }

    // Role check for status updates: Director is read-only; Admin can transition
    const updateBox = document.getElementById("adminUpdateControlsBox");
    if (currentUser.role === "director") {
      updateBox.classList.add("hidden");
    } else {
      updateBox.classList.remove("hidden");
      document.getElementById("modalNewStatus").value = app.status === "Submitted" ? "Under Review" : (app.status === "Under Review" ? "Accepted" : app.status);
      document.getElementById("modalRemarks").value = "";
    }

    modal.classList.remove("hidden");
  } catch (err) {
    showToast(err.message, "error");
  }
}

function closeDetailModal() {
  document.getElementById("appDetailModal").classList.add("hidden");
  activeModalAppId = null;
}

// FR-19: Submit Status Update
async function submitStatusUpdate() {
  if (!activeModalAppId) return;

  const new_status = document.getElementById("modalNewStatus").value;
  const remarks = document.getElementById("modalRemarks").value.trim();

  try {
    const res = await fetch(`${API_BASE}/api/admin/applications/${activeModalAppId}/status`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${currentToken}`
      },
      body: JSON.stringify({ new_status, remarks })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Status update failed");

    showToast(data.message, "success");
    closeDetailModal();
    loadAdminDashboard();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// FR-12: Export Applications CSV
function exportApplicationsCSV() {
  const course = document.getElementById("filterCourseSelect")?.value || "";
  const status = document.getElementById("filterStatusSelect")?.value || "";

  let url = `${API_BASE}/api/admin/export-csv?`;
  if (course) url += `course=${encodeURIComponent(course)}&`;
  if (status) url += `status=${encodeURIComponent(status)}&`;

  fetch(url, {
    headers: { "Authorization": `Bearer ${currentToken}` }
  })
  .then(res => {
    if (!res.ok) throw new Error("CSV Export failed");
    return res.blob();
  })
  .then(blob => {
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = `IEM_Admissions_Report_${new Date().toISOString().slice(0,10)}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast("CSV report generated and downloaded successfully.", "success");
  })
  .catch(err => showToast(err.message, "error"));
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
