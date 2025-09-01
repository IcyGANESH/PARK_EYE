"use client"

import * as React from "react"
import { toast as sonnerToast } from "sonner"

export function useToast() {
  const toast = React.useCallback(
    (message: string, type: "success" | "error" | "info" = "info") => {
      switch (type) {
        case "success":
          sonnerToast.success(message)
          break
        case "error":
          sonnerToast.error(message)
          break
        default:
          sonnerToast(message)
      }
    },
    []
  )

  return { toast }
}
