(let (lambda λ)) ;; Alias a ASCII name for `λ`.

(define macro (apply f l)
  (eval (unshift (eval f) (eval l))))