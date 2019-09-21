
/***********************************************************************************
 *                                                                                 *
 * TSPLEAP - A GENERATOR FOR LEAPER GRAPHS                                         *
 *                                                                                 *
 * by Michael Juenger and Giovanni Rinaldi                                         *
 *                                                                                 *
 * November 1994                                                                   *
 *                                                                                 *
 * One of the earliest trips of a traveling salesman, as we would call it today,   *
 * was the closed trip of a knight ({1,2}-leaper)) on a chessboard, visiting each  *
 * of the 64 squares exactly once, and it was discovered by Euler in 1759 [E].     *
 *                                                                                 *
 * Since then the (recreational) mathematical literature has often dealt with      *
 * similar questions as the one Euler answered in the affirmative for an "ordinary *
 * leaper" on an "ordinary chessboard":                                            *
 *                                                                                 *
 *   Can a leaper, starting at any square of the board, visit each other           *
 *   square exactly once and return to its starting square?                        *
 *                                                                                 *
 * In the November 1994 issue of the Mathematical Gazette, there is an article     *
 * by D. E. Knuth [K] in which he discusses conditions on whether there exists     *
 * an {r,s}-leaper on an mxn board or not. (An "ordinary leaper" on an "ordinary   *
 * board" is a {1,2}-leaper on a 8x8 board.) Of course, the question is, in        *
 * "tsp"-language:                                                                 *
 *                                                                                 *
 *   Is the graph, whose nodes are the squares, and whose edges represent          *
 *   the legal moves of the leaper, hamiltonian?                                   *
 *                                                                                 *
 * In his article, Knuth remarks that this type of problem might be an interesting *
 * challenge for computer codes for the symmetric traveling salesrep problem.      *
 *                                                                                 *
 * Anyone who likes to make such experiments can use this simple program to        *
 * generate instances in TSPLIB format. This file should be "tspleap.c", and one   *
 * can generate an executable named "tspleap", e.g. under UNIX via the command     *
 * "cc -o tspleap tspleap.c". The command to generate an instance is of the form:  *
 *                                                                                 *
 *   tspleap r s m n                                                               *
 *                                                                                 *
 * The program then generates the according TSPLIB file for an {r,s}-leaper        *
 * on a mxn board in the local working directory (usually TSPLIB),                 *
 *                                                                                 *
 *   e.g. "tspleap 1 2 8 8" generates the file "leaper_1_2_8_8.tsp".               *
 *                                                                                 *
 * The instance consists of a complete graph on mxn nodes, in which the edges      *
 * corresponding to legal leaper moves have weight 0, and the remaining edges      *
 * weight 1. If a solution has value 0, the graph is hamiltonian and the tour      *
 * proves it, if an optimum solution has a value k greater than 0, then k is the   *
 * minimum number of edges that must be added to the leaper graph in order to make *
 * it hamiltonian.                                                                 *
 *                                                                                 *
 * The authors did a few sample runs with the programs described in [JRR]. E.g.,   *
 * there is no {6,7}-leaper tour on a 13x76 board, and at least 18 edges have to   *
 * be added to the corresponding graph in order to make it hamiltonian. On the     *
 * other hand, there is, e.g., a {7,8}-leaper tour on a 15x106-board. Try to       *
 * find it!                                                                        *  
 *                                                                                 *
 * [E]   Leonhard Euler, Solution d'une question curieuse qui ne paroit soumise    *
 *       a aucune analyse, Memoires de l'Academie Royale des Sciences et Belles    *
 *       Lettres, Berlin, 1759, 310-337.                                           *
 *                                                                                 *
 * [K]   Donald E. Knuth, Leaper Graphs, Mathematical Gazette (1994). to appear    *
 *                                                                                 *
 * [JRR] Michael Juenger, Gerhard Reinelt, and Giovanni Rinaldi, The Traveling     *
 *       Salesman Problem, Report R. 375, IASI-CNR Rome, to appear in M. Ball,     *
 *       T. Magnanti, C.L. Monma, and G. Nemhauser (eds.), Handbook on Operations  *
 *       Research and Management Sciences: Networks, North Holland, 1994           *
 *                                                                                 *
 ***********************************************************************************/

#include <stdio.h>
void main(argc,argv)
 int  argc;
 char **argv;
{
 int m,n,r,s,i,j,k,l;
 char   ofname[100];
 FILE   *of;
 sscanf(argv[1],"%d",&r); sscanf(argv[2],"%d",&s);
 sscanf(argv[3],"%d",&m); sscanf(argv[4],"%d",&n);
 sprintf(ofname,"leaper_%d_%d_%d_%d.tsp",r,s,m,n);
 if (!(of = fopen(ofname,"w"))) { printf(" Cannot open %s.\n",ofname); exit(1); }
 fprintf(of,"NAME: leaper_%d_%d_%d_%d\n",r,s,m,n);
 fprintf(of,"TYPE: TSP\n");
 fprintf(of,"COMMENT: (%d,%d) leaper on a %dx%d board\n",r,s,m,n);
 fprintf(of,"DIMENSION: %d\n",m*n);
 fprintf(of,"EDGE_WEIGHT_TYPE: EXPLICIT\n");
 fprintf(of,"EDGE_WEIGHT_FORMAT: UPPER_ROW \n");
 fprintf(of,"EDGE_WEIGHT_SECTION\n");
 for (i=1; i<=m; i++) for (j=1; j<=(i<m?n:n-1); j++)
  for (k=(j<n?i:i+1); k<=m; k++) for (l=(i<k?1:j+1); l<=n; l++)      
   fprintf(of," %1d\n",
              ((k!=i+r)||((l!=j+s)&&(l!=j-s)))&&((k!=i+s)||((l!=j+r)&&(l!=j-r))));
 exit(0);
}
