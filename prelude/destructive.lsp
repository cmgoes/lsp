(define macro (incr! sym n)
  (mutate (sym (+ (eval sym) (eval n)))))

(define macro (decr! sym n)
  (mutate (sym (- (eval sym) (eval n)))))

(define macro (+1 sym)
  (mutate (sym (+ (eval sym) 1))))

(define macro (-1 sym)
  (mutate (sym (- (eval sym) 1))))