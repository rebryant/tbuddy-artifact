/*========================================================================
  Copyright (c) 2022 Randal E. Bryant, Carnegie Mellon University
  
  As noted below, this code is a modified version of code authored and
  copywrited by Jorn Lind-Nielsen.  Permisssion to use the original
  code is subject to the terms noted below.

  Regarding the modifications, and subject to any constraints on the
  use of the original code, permission is hereby granted, free of
  charge, to any person obtaining a copy of this software and
  associated documentation files (the "Software"), to deal in the
  Software without restriction, including without limitation the
  rights to use, copy, modify, merge, publish, distribute, sublicense,
  and/or sell copies of the Software, and to permit persons to whom
  the Software is furnished to do so, subject to the following
  conditions:
  
  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
  ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
========================================================================*/


/*========================================================================
               Copyright (C) 1996-2002 by Jorn Lind-Nielsen
                            All rights reserved

    Permission is hereby granted, without written agreement and without
    license or royalty fees, to use, reproduce, prepare derivative
    works, distribute, and display this software and its documentation
    for any purpose, provided that (1) the above copyright notice and
    the following two paragraphs appear in all copies of the source code
    and (2) redistributions, including without limitation binaries,
    reproduce these notices in the supporting documentation. Substantial
    modifications to this software may be copyrighted by their authors
    and need not follow the licensing terms described here, provided
    that the new terms are clearly indicated in all files where they apply.

    IN NO EVENT SHALL JORN LIND-NIELSEN, OR DISTRIBUTORS OF THIS
    SOFTWARE BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
    INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF THIS
    SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE AUTHORS OR ANY OF THE
    ABOVE PARTIES HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    JORN LIND-NIELSEN SPECIFICALLY DISCLAIM ANY WARRANTIES, INCLUDING,
    BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
    FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS
    ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE NO
    OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
    MODIFICATIONS.
========================================================================*/

/*************************************************************************
  $Header: /cvsroot/buddy/buddy/src/kernel.h,v 1.2 2004/07/13 20:51:49 haimcohen Exp $
  FILE:  kernel.h
  DESCR: Kernel specific definitions for BDD package
  AUTH:  Jorn Lind
  DATE:  (C) june 1997
*************************************************************************/

#ifndef _KERNEL_H
#define _KERNEL_H

/** Enabling proof generation **/
#ifndef ENABLE_TBDD
#define ENABLE_TBDD 0
#endif

/*=== Includes =========================================================*/

#include <limits.h>
#include <setjmp.h>

#if ENABLE_TBDD
#include "tbdd.h"
#include "prover.h"
#else
#include "bdd.h"
#endif

/*=== Error message destination ===*/
#define ERROUT stdout

#if ENABLE_TBDD
/*=== ERROR CHECKING =========*/

#ifndef DO_TRACE
#define DO_TRACE 0
#endif

#if DO_TRACE
/* Track activity of specified clause */
#define TRACE_CLAUSE  17379
/* Track activity of specified node xvar */
#define TRACE_NNAME 2881
#endif /* DO_TRACE */
#endif /* TBDD */

/*=== SANITY CHECKS ====================================================*/

   /* Make sure we use at least 32 bit integers */
#if (INT_MAX < 0x7FFFFFFF)
#error The compiler does not support 4 byte integers!
#endif


   /* Sanity check argument and return eventual error code */
#define CHECK(r)\
   if (!bddrunning) return bdd_error(BDD_RUNNING);\
   else if ((r) < 0  ||  (r) >= bddnodesize) return bdd_error(BDD_ILLBDD);\
   else if (r >= 2 && LOW(r) == -1) return bdd_error(BDD_ILLBDD)\

   /* Sanity check argument and return eventually the argument 'a' */
#define CHECKa(r,a)\
   if (!bddrunning) { bdd_error(BDD_RUNNING); return (a); }\
   else if ((r) < 0  ||  (r) >= bddnodesize)\
     { bdd_error(BDD_ILLBDD); return (a); }\
   else if (r >= 2 && LOW(r) == -1)\
     { bdd_error(BDD_ILLBDD); return (a); }

#define CHECKn(r)\
   if (!bddrunning) { bdd_error(BDD_RUNNING); return; }\
   else if ((r) < 0  ||  (r) >= bddnodesize)\
     { bdd_error(BDD_ILLBDD); return; }\
   else if (r >= 2 && LOW(r) == -1)\
     { bdd_error(BDD_ILLBDD); return; }


/*=== SEMI-INTERNAL TYPES ==============================================*/

typedef struct s_BddNode /* Node table entry */
{
   unsigned int refcou : 10;
   unsigned int level  : 22;
   int low;
   int high;
   int hash;
   int next;
#if ENABLE_TBDD
   int xvar;     /* Associated extension variable */
   int dclause;  /* Base index of defining clause */
#endif /* ENABLE_TBDD */
} BddNode;


/*=== KERNEL VARIABLES =================================================*/

#ifdef CPLUSPLUS
extern "C" {
#endif

extern int       bddrunning;         /* Flag - package initialized */
extern int       bdderrorcond;       /* Some error condition was met */
extern int       bddnodesize;        /* Number of allocated nodes */
extern int       bddmaxnodesize;     /* Maximum allowed number of nodes */
extern int       bddmaxnodeincrease; /* Max. # of nodes used to inc. table */
extern BddNode*  bddnodes;           /* All of the bdd nodes */
extern int       bddvarnum;          /* Number of defined BDD variables */
extern int*      bddrefstack;        /* Internal node reference stack */
extern int*      bddrefstacktop;     /* Internal node reference stack top */
extern int*      bddvar2level;
extern int*      bddlevel2var;
extern jmp_buf   bddexception;
extern int       bddreorderdisabled;
extern int       bddresized;
extern bddCacheStat bddcachestats;

#ifdef CPLUSPLUS
}
#endif


/*=== KERNEL DEFINITIONS ===============================================*/

/* 
   Note: Although have 22 bits allocated for variable, upper bit
   required for mark bit used in GC.  That leaves 21 bits available
   for actual level number
 */
#define MAXVAR 0x1FFFFF
#define MAXREF 0x3FF

   /* Reference counting */
#define DECREF(n) if (bddnodes[n].refcou!=MAXREF && bddnodes[n].refcou>0) bddnodes[n].refcou--
#define INCREF(n) if (bddnodes[n].refcou<MAXREF) bddnodes[n].refcou++
#define DECREFp(n) if (n->refcou!=MAXREF && n->refcou>0) n->refcou--
#define INCREFp(n) if (n->refcou<MAXREF) n->refcou++
#define HASREF(n) (bddnodes[n].refcou > 0)

   /* Marking BDD nodes */
#define MARKON   0x200000    /* Bit used to mark a node (1) */
#define MARKOFF  0x1FFFFF    /* - unmark */
#define MARKHIDE 0x1FFFFF
#define SETMARK(n)  (bddnodes[n].level |= MARKON)
#define UNMARK(n)   (bddnodes[n].level &= MARKOFF)
#define MARKED(n)   (bddnodes[n].level & MARKON)
#define SETMARKp(p) (node->level |= MARKON)
#define UNMARKp(p)  (node->level &= MARKOFF)
#define MARKEDp(p)  (node->level & MARKON)

   /* Hashfunctions */

#define PAIR(a,b)      ((unsigned int)((((unsigned int)a)+((unsigned int)b))*(((unsigned int)a)+((unsigned int)b)+((unsigned int)1))/((unsigned int)2)+((unsigned int)a)))
#define TRIPLE(a,b,c)  ((unsigned int)(PAIR((unsigned int)c,PAIR(a,b))))

   /* Inspection of BDD nodes */
#define ISCONST(a) ((a) < 2)
#define ISNONCONST(a) ((a) >= 2)
#define ISONE(a)   ((a) == 1)
#define ISZERO(a)  ((a) == 0)
#define LEVEL(a)   (bddnodes[a].level)
#define LOW(a)     (bddnodes[a].low)
#define HIGH(a)    (bddnodes[a].high)
#define LEVELp(p)   ((p)->level)
#define LOWp(p)     ((p)->low)
#define HIGHp(p)    ((p)->high)

#if ENABLE_TBDD
#define XVAR(a)      (bddnodes[a].xvar)
#define DCLAUSE(a)   (bddnodes[a].dclause)
#define XVARp(p)     ((p)->xvar)
#define DCLAUSEp(p)  ((p)->dclause)
#define NNAME(a) ((a) < 2?(a):XVAR(a))
#endif /* ENABLE_TBDD */


   /* Stacking for garbage collector */
#define INITREF    bddrefstacktop = bddrefstack
#define PUSHREF(a) *(bddrefstacktop++) = (a)
#define READREF(a) *(bddrefstacktop-(a))
#define POPREF(a)  bddrefstacktop -= (a)

#define BDDONE 1
#define BDDZERO 0

#ifndef CLOCKS_PER_SEC
  /* Pass `CPPFLAGS=-DDEFAULT_CLOCK=1000' as an argument to ./configure
     to override this setting.  */
# ifndef DEFAULT_CLOCK
#  define DEFAULT_CLOCK 60
# endif
# define CLOCKS_PER_SEC DEFAULT_CLOCK
#endif

#define DEFAULTMAXNODEINC 50000

#define MIN(a,b) ((a) < (b) ? (a) : (b))
#define MAX(a,b) ((a) > (b) ? (a) : (b))
#define ABS(a) ((a)<0?-(a):(a))
#define NEW(t,n) ( (t*)malloc(sizeof(t)*(n)) )


/*=== KERNEL PROTOTYPES ================================================*/

#ifdef CPLUSPLUS
extern "C" {
#endif

extern int    bdd_error(int);
extern int    bdd_makenode(unsigned int, int, int);
extern int    bdd_noderesize(int);
extern void   bdd_checkreorder(void);
extern void   bdd_mark(int);
extern void   bdd_mark_upto(int, int);
extern void   bdd_markcount(int, int*);
extern void   bdd_unmark(int);
extern void   bdd_unmark_upto(int, int);
extern void   bdd_register_pair(bddPair*);
extern int   *fdddec2bin(int, int);

extern int    bdd_operator_init(int);
extern void   bdd_operator_done(void);
extern void   bdd_operator_varresize(void);
extern void   bdd_operator_reset(void);

extern void   bdd_pairs_init(void);
extern void   bdd_pairs_done(void);
extern int    bdd_pairs_resize(int,int);
extern void   bdd_pairs_vardown(int);

extern void   bdd_fdd_init(void);
extern void   bdd_fdd_done(void);

extern void   bdd_reorder_init(void);
extern void   bdd_reorder_done(void);
extern int    bdd_reorder_ready(void);
extern void   bdd_reorder_auto(void);
extern int    bdd_reorder_vardown(int);
extern int    bdd_reorder_varup(int);

extern void   bdd_cpp_init(void);

#ifdef CPLUSPLUS
}
#endif

#if ENABLE_TBDD
/* Proof generation interface */

/* Data type for proof-generating operations */
typedef struct {
    BDD root;
    int clause_id;
} pcbdd;

/* In file prover.c */
/* Complete proof of apply operation */
/* Absolute of returned value indicates the ID of the justifying proof step */
/* Value will be < 0 when previous clause ID also used as intermediate step */
extern int justify_apply(int op, BDD l, BDD r, int splitVar, pcbdd tresl, pcbdd tresh, BDD res);

/* In file bddop.c */
/* Low-level functions to implement operations on TBDDs */
pcbdd      bdd_and_justify(BDD, BDD);    
pcbdd      bdd_imptst_justify(BDD, BDD);    
pcbdd      bdd_and_imptst_justify(BDD, BDD, BDD);    

#endif

#endif /* _KERNEL_H */


/* EOF */
