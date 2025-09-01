"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useToast } from "../../../hooks/use-toast"
import { Camera, MapPin, AlertTriangle, Upload } from "lucide-react"

const crimeTypes = ["Theft", "Vandalism", "Hit and Run", "Reckless Driving", "Drug Related", "Assault", "Other"]

export default function CrimeReportForm() {
  const router = useRouter()
  const { toast } = useToast()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [formData, setFormData] = useState({
    vehicleNumber: "",
    location: "",
    crimeType: "",
    extraInfo: "",
    image: null as File | null,
  })
  const [errors, setErrors] = useState<Record<string, string>>({})

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }))
    }
  }

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        // 5MB limit
        setErrors((prev) => ({ ...prev, image: "Image size must be less than 5MB" }))
        return
      }
      setFormData((prev) => ({ ...prev, image: file }))
      setErrors((prev) => ({ ...prev, image: "" }))
    }
  }

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.vehicleNumber.trim()) {
      newErrors.vehicleNumber = "Vehicle number is required"
    }

    if (!formData.location.trim()) {
      newErrors.location = "Location is required"
    }

    if (!formData.crimeType) {
      newErrors.crimeType = "Please select a crime type"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) {
      toast
      return
    }

    setIsSubmitting(true)

    try {
      // Get user_id from localStorage
      const userId = localStorage.getItem("user_id")
      if (!userId) {
        toast
        setIsSubmitting(false)
        return
      }

      // Create FormData for API submission
      const submitData = new FormData()
      submitData.append("user_id", userId)
      submitData.append("vehicle_number", formData.vehicleNumber)
      submitData.append("location", formData.location)
      submitData.append("crime_type", formData.crimeType)
      submitData.append("extra_info", formData.extraInfo)

      if (formData.image) {
        submitData.append("image", formData.image)
      }

      // Submit to API
      const response = await fetch("/api/crime-reports", {
        method: "POST",
        body: submitData,
      })

      if (!response.ok) {
        throw new Error("Failed to submit report")
      }

      const result = await response.json()

      toast

      // Redirect to success page
      router.push("/success")
    } catch (error) {
      console.error("Error submitting report:", error)
      toast
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="mx-auto max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-4">
            <AlertTriangle className="h-8 w-8 text-primary" />
            <h1 className="text-2xl font-bold text-balance">Report a Vehicle Involved in a Crime</h1>
          </div>
          <p className="text-muted-foreground text-pretty">
            Your report is confidential and helps keep our community safe.
          </p>
        </div>

        {/* Form */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Report Details</CardTitle>
            <CardDescription>Please provide as much information as possible</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Vehicle Number */}
              <div className="space-y-2">
                <Label htmlFor="vehicleNumber" className="flex items-center gap-2">
                  <span>Vehicle Number *</span>
                </Label>
                <Input
                  id="vehicleNumber"
                  placeholder="e.g., ABC-1234"
                  value={formData.vehicleNumber}
                  onChange={(e) => handleInputChange("vehicleNumber", e.target.value)}
                  className={errors.vehicleNumber ? "border-destructive" : ""}
                />
                {errors.vehicleNumber && <p className="text-sm text-destructive">{errors.vehicleNumber}</p>}
              </div>

              {/* Location */}
              <div className="space-y-2">
                <Label htmlFor="location" className="flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  <span>Location *</span>
                </Label>
                <Input
                  id="location"
                  placeholder="Street address or landmark"
                  value={formData.location}
                  onChange={(e) => handleInputChange("location", e.target.value)}
                  className={errors.location ? "border-destructive" : ""}
                />
                {errors.location && <p className="text-sm text-destructive">{errors.location}</p>}
              </div>

              {/* Crime Type */}
              <div className="space-y-2">
                <Label htmlFor="crimeType">Crime Type *</Label>
                <Select value={formData.crimeType} onValueChange={(value) => handleInputChange("crimeType", value)}>
                  <SelectTrigger className={errors.crimeType ? "border-destructive" : ""}>
                    <SelectValue placeholder="Select crime type" />
                  </SelectTrigger>
                  <SelectContent>
                    {crimeTypes.map((crime) => (
                      <SelectItem key={crime} value={crime}>
                        {crime}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {errors.crimeType && <p className="text-sm text-destructive">{errors.crimeType}</p>}
              </div>

              {/* Image Upload */}
              <div className="space-y-2">
                <Label htmlFor="image" className="flex items-center gap-2">
                  <Camera className="h-4 w-4" />
                  <span>Photo Evidence (Optional)</span>
                </Label>
                <div className="relative">
                  <Input
                    id="image"
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-primary file:text-primary-foreground hover:file:bg-primary/90"
                  />
                  {formData.image && (
                    <p className="text-sm text-muted-foreground mt-1">Selected: {formData.image.name}</p>
                  )}
                </div>
                {errors.image && <p className="text-sm text-destructive">{errors.image}</p>}
                <p className="text-xs text-muted-foreground">
                  Maximum file size: 5MB. Supported formats: JPG, PNG, GIF
                </p>
              </div>

              {/* Extra Info */}
              <div className="space-y-2">
                <Label htmlFor="extraInfo">Additional Information</Label>
                <Textarea
                  id="extraInfo"
                  placeholder="Any additional details that might be helpful..."
                  value={formData.extraInfo}
                  onChange={(e) => handleInputChange("extraInfo", e.target.value)}
                  rows={4}
                  className="resize-none"
                />
                <p className="text-xs text-muted-foreground text-right">{formData.extraInfo.length}/500 characters</p>
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <div className="flex items-center gap-2">
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                    Submitting Report...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <Upload className="h-4 w-4" />
                    Submit Report
                  </div>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Privacy Notice */}
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription className="text-sm">
            All reports are treated confidentially. False reporting is a serious offense. Only submit genuine crime
            reports.
          </AlertDescription>
        </Alert>
      </div>
    </div>
  )
}
