import { CheckCircle, Home, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"

export default function ReportSuccessPage() {
  return (
    <div className="min-h-screen bg-background p-4 flex items-center justify-center">
      <div className="mx-auto max-w-md">
        <Card>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <CheckCircle className="h-16 w-16 text-accent" />
            </div>
            <CardTitle className="text-2xl text-balance">Report Submitted Successfully</CardTitle>
            <CardDescription className="text-pretty">
              Thank you for helping keep our community safe. Your report has been received and will be reviewed by the
              appropriate authorities.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-muted p-4 rounded-lg">
              <h3 className="font-semibold mb-2">What happens next?</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Your report will be reviewed within 24 hours</li>
                <li>• Authorities will be notified if immediate action is required</li>
                <li>• You may be contacted for additional information</li>
              </ul>
            </div>

            <div className="flex flex-col gap-3">
              <Button asChild className="w-full">
                <Link href="/" className="flex items-center gap-2">
                  <Home className="h-4 w-4" />
                  Return to Home
                </Link>
              </Button>

              <Button variant="outline" asChild className="w-full bg-transparent">
                <Link href="/complain" className="flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  Submit Another Report
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
