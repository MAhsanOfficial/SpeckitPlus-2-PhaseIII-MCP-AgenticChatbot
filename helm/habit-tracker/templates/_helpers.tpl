{{/*
Expand the name of the chart.
*/}}
{{- define "habit-tracker.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "habit-tracker.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "habit-tracker.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "habit-tracker.labels" -}}
helm.sh/chart: {{ include "habit-tracker.chart" . }}
{{ include "habit-tracker.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "habit-tracker.selectorLabels" -}}
app.kubernetes.io/name: {{ include "habit-tracker.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "habit-tracker.backend.labels" -}}
{{ include "habit-tracker.labels" . }}
app: habit-tracker-backend
component: backend
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "habit-tracker.frontend.labels" -}}
{{ include "habit-tracker.labels" . }}
app: habit-tracker-frontend
component: frontend
{{- end }}
