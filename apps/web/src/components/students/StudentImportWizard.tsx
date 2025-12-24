'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { importService, ImportPreviewResponse, ImportRowStatus } from '@/utils/import-service';
import { Upload, CheckCircle, AlertTriangle, FileText, Download } from 'lucide-react';

export default function StudentImportWizard() {
    const [step, setStep] = useState(1);
    const [file, setFile] = useState<File | null>(null);
    const [previewData, setPreviewData] = useState<ImportPreviewResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [importResult, setImportResult] = useState<any>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUploadPreview = async () => {
        if (!file) return;
        setIsLoading(true);
        try {
            const data = await importService.uploadPreview(file);
            setPreviewData(data);
            setStep(2);
        } catch (error) {
            console.error('Preview failed', error);
            alert('Failed to parse file. Please check format.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleExecuteImport = async () => {
        if (!previewData || !file) return;
        if (!confirm(`Are you sure you want to import ${previewData.valid_count} students?`)) return;

        setIsLoading(true);
        try {
            const result = await importService.executeImport(previewData, file.name);
            setImportResult(result);
            setStep(3);
        } catch (error) {
            console.error('Import failed', error);
            alert('Import execution failed.');
        } finally {
            setIsLoading(false);
        }
    };

    const downloadTemplate = async () => {
        setIsLoading(true);
        try {
            await importService.downloadTemplate();
        } catch (error) {
            alert("Failed to download template");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="space-y-6 max-w-5xl mx-auto">
            <h1 className="text-2xl font-bold text-gray-900">Bulk Student Import</h1>

            {/* Steps Indicator */}
            <div className="flex justify-between mb-8 max-w-xl mx-auto">
                {[1, 2, 3].map((s) => (
                    <div key={s} className={`flex items-center gap-2 ${step >= s ? 'text-blue-600 font-bold' : 'text-gray-400'}`}>
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${step >= s ? 'border-blue-600 bg-blue-50' : 'border-gray-300'}`}>
                            {s}
                        </div>
                        <span>{s === 1 ? 'Upload' : s === 2 ? 'Preview' : 'Result'}</span>
                    </div>
                ))}
            </div>

            {/* Step 1: Upload */}
            {step === 1 && (
                <Card>
                    <CardHeader>
                        <h3 className="text-lg font-medium">Step 1: Upload File</h3>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="p-6 border-2 border-dashed border-gray-300 rounded-lg text-center space-y-4">
                            <Upload className="mx-auto text-gray-400" size={48} />
                            <p className="text-gray-600">Drag and drop your Excel/CSV file here, or click to browse</p>
                            <input
                                type="file"
                                accept=".csv, .xlsx, .xls"
                                onChange={handleFileChange}
                                className="hidden"
                                id="file-upload"
                            />
                            <label htmlFor="file-upload">
                                <span className="inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed border border-gray-300 bg-transparent hover:bg-gray-50 focus:ring-indigo-500 text-gray-700 px-4 py-2 text-sm cursor-pointer">
                                    Browse Files
                                </span>
                            </label>
                            {file && <p className="text-sm font-medium text-green-600 mt-2">Selected: {file.name}</p>}
                        </div>

                        <div className="flex justify-between items-center bg-blue-50 p-4 rounded-md">
                            <div className="flex items-center gap-3">
                                <FileText className="text-blue-500" />
                                <div>
                                    <p className="font-medium text-sm">Need a template?</p>
                                    <p className="text-xs text-gray-500">Download the standard format to avoid errors.</p>
                                </div>
                            </div>
                            <Button variant="outline" size="sm" onClick={downloadTemplate} className="gap-2">
                                <Download size={16} /> Download Template
                            </Button>
                        </div>

                        <div className="flex justify-end">
                            <Button onClick={handleUploadPreview} disabled={!file || isLoading}>
                                {isLoading ? 'Processing...' : 'Next: Preview Data'}
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Step 2: Preview */}
            {step === 2 && previewData && (
                <Card>
                    <CardHeader>
                        <div className="flex justify-between items-center">
                            <h3 className="text-lg font-medium">Step 2: Validation Preview</h3>
                            <div className="flex gap-4 text-sm">
                                <span className="text-green-600 font-bold">{previewData.valid_count} Valid</span>
                                <span className="text-red-600 font-bold">{previewData.invalid_count} Invalid</span>
                                <span className="text-orange-600 font-bold">{previewData.duplicate_count} Duplicates</span>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="border rounded-md overflow-x-auto max-h-[500px]">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-gray-50 text-gray-700 sticky top-0">
                                    <tr>
                                        <th className="p-3 border-b">Row</th>
                                        <th className="p-3 border-b">Name</th>
                                        <th className="p-3 border-b">Admission No</th>
                                        <th className="p-3 border-b">Course</th>
                                        <th className="p-3 border-b">Status</th>
                                        <th className="p-3 border-b">Errors</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {previewData.rows.map((row, idx) => (
                                        <table className="contents" key={idx}>
                                            <tr className="hover:bg-gray-50 border-b">
                                                <td className="p-3">{row.row_number}</td>
                                                <td className="p-3 font-medium">{row.data.name}</td>
                                                <td className="p-3">{row.data.admission_number}</td>
                                                <td className="p-3">{row.data.course_code}</td>
                                                <td className="p-3">
                                                    {row.status === ImportRowStatus.VALID && <span className="text-green-600 font-bold flex items-center gap-1"><CheckCircle size={14} /> Valid</span>}
                                                    {row.status === ImportRowStatus.INVALID && <span className="text-red-600 font-bold flex items-center gap-1"><AlertTriangle size={14} /> Invalid</span>}
                                                    {row.status === ImportRowStatus.DUPLICATE && <span className="text-orange-600 font-bold flex items-center gap-1"><AlertTriangle size={14} /> Duplicate</span>}
                                                </td>
                                                <td className="p-3 text-red-500 text-xs">
                                                    {row.errors.map(e => `${e.field}: ${e.message}`).join(', ')}
                                                </td>
                                            </tr>
                                        </table>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        <div className="flex justify-between">
                            <Button variant="outline" onClick={() => setStep(1)} disabled={isLoading}>Back</Button>
                            <Button onClick={handleExecuteImport} disabled={isLoading || previewData.valid_count === 0}>
                                {isLoading ? 'Importing...' : `Import ${previewData.valid_count} Students`}
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Step 3: Result */}
            {step === 3 && importResult && (
                <Card>
                    <CardHeader>
                        <h3 className="text-lg font-medium text-center text-green-600">Import Completed!</h3>
                    </CardHeader>
                    <CardContent className="text-center space-y-6">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                            <CheckCircle className="text-green-600" size={40} />
                        </div>

                        <div className="grid grid-cols-3 gap-4 max-w-lg mx-auto bg-gray-50 p-6 rounded-lg">
                            <div>
                                <p className="text-2xl font-bold text-gray-900">{importResult.log_id}</p>
                                <p className="text-xs text-gray-500 uppercase">Log ID</p>
                            </div>
                            <div>
                                <p className="text-2xl font-bold text-green-600">{previewData?.valid_count}</p>
                                <p className="text-xs text-gray-500 uppercase">Imported</p>
                            </div>
                            <div>
                                <p className="text-2xl font-bold text-red-600">{previewData?.invalid_count}</p>
                                <p className="text-xs text-gray-500 uppercase">Failed</p>
                            </div>
                        </div>

                        <div className="flex justify-center gap-4">
                            <Button variant="outline" onClick={() => window.location.reload()}>Import More</Button>
                            <Button onClick={() => window.location.href = '/students'}>Go to Student List</Button>
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
