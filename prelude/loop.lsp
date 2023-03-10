(define macro (while c b)
  (iterate (do
    (unless (eval c) break)
    (eval b))))

(define macro (until c b)
  (while (! (eval c)) (eval b)))

(define macro (loop b)
  (iterate (eval b)))

(define (from n m f)
  (unless (> n m) (do
    (f n)
    (from (+ n 1) m f))))

(define (times n f) (from 0 (- n 1) f))