(define macro (quote expression) expression)

(let (append  push)
     (prepend unshift)
     (merge  concat)
     (merge! concat!))

(define (empty? l) (= (size l) 0))

(define (first l) (index    0  l))
(define (last  l) (index (- 1) l))

(let (head first))
(define (tail l) (shift l))

(define (each l cb) (do
  (times (size l) (-> (cb (index %1 l))))
  (yield l)))

(define macro (for sym in l body) (do
  (let (__i 0) (__array (eval l)))
  (while (< __i (size __array)) (do
    (mutate (sym (index __i __array)))
    (eval body)
    (+1 __i)))
  (delete __i __array sym)
  (eval l)))

(define (take n l) (do  ;; Takes the first n elements of list l.
  (let (new (list)) (i 0))
  (while (< i n) (do
    (push (index i l) new)
    (+1 i)))
  (yield new)))

(define (drop n l) (do  ;; Drops the first n elements of list l.
  (let (len (size l)) (new (list)) (i n))
  (while (< i len) (do 
    (push (index i l) new)
    (+1 i)))
  (yield new)))

(define (reverse l) (do
  (let (reversed (list)))
  (until (empty? l) (do
    (push (last l) reversed)
    (pop l)))
  (yield reversed)))

(define (fill l n m)
  (unless (< m n)
    (fill (push n l) (+ n 1) m)
    l))

(define (range n m) (fill '() n m))

(define (map f l)
  (unless (empty? l)
    (concat (list (f (head l))) (map f (tail l)))
    (list)))

(define (reduce f acc l)
  (unless (empty? l)
    (reduce f (f acc (head l)) (tail l))
    acc))

(define (filter f l) (do
  (let (new (list)))
  (for e in l (do
    (if (f e) (push e new))))
  (yield new)))